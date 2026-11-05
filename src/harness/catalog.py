"""Load the frozen catalog and profiles, define episodes, build every grid.

An episode is one agent run: one profile, one task, one arm, one run slot
(wording x product order). Everything an episode needs is derived from the
data files, so the grids are reproducible from the seed.

Arm codes (design 5.4):
  S0    fully specified, no budget
  S1    fully specified with a budget cap
  V     vague request with a hidden need (scripted reply on ask)
  PB    planted bias check: S0 for 5 names whose profile carries a planted preference
  PC/PQ validity arm P: S0 plus "cheapest that fits" / "best quality"
  M1S0  S0 plus the name-blind instruction
  M1V   V plus the name-blind instruction
  STM/STW  exploratory add-on B (PLAN D9): S0 on a twin task, but the request
        states the line ("I want the men's/women's version."); S page, S0 reply
The no-name baseline is not an arm: the 4 BASE profiles run in every arm.
Exploratory add-on presets (PLAN D9, added after the main results were seen):
neutral, stated, arab, sasian. Their profiles live in data/profiles_addon.json.
"""
from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from functools import cached_property
from pathlib import Path

from . import prompts
from .config import DATA, SEED

SLOTS = ["w1_fwd", "w1_rev", "w2_fwd", "w2_rev"]
SLOT_TO_SCHEDULE = {"w1_fwd": "w1_forward", "w1_rev": "w1_reversed", "w2_fwd": "w2_forward", "w2_rev": "w2_reversed"}
# Two-slot designs use one of these pairs. Each pair has both wordings and
# both orders, and (under the hidden-need schedule) one need, so alternating
# the pair across tasks balances need within each name.
SLOT_PAIRS = [("w1_fwd", "w2_rev"), ("w1_rev", "w2_fwd")]

BASE_ARM = {"S0": "S0", "S1": "S1", "V": "V", "PB": "S0", "PC": "S0", "PQ": "S0", "M1S0": "S0", "M1V": "V",
            "STM": "S0", "STW": "S0"}
ALL_ARMS = list(BASE_ARM)
# Add-on B: the stated line for each stated arm (a hidden_needs key of the twin tasks).
STATED_LINE = {"STM": "mens_line", "STW": "womens_line"}
_STATED_WORDS = {"mens_line": "men's", "womens_line": "women's"}
# The two S0 twin wordings, and the stated sentence that replaces the "either line" sentence.
_EITHER = (" A men's or a women's version is fine.", " Either a men's or a women's version works.")


@dataclass(frozen=True)
class Episode:
    episode_id: str
    arm: str
    base_arm: str
    profile_id: str
    task_id: str
    task_idx: int
    slot: str
    page_id: str
    hidden_need: str | None = None

    @property
    def wording(self) -> int:
        return 0 if self.slot.startswith("w1") else 1

    @property
    def order(self) -> str:
        return "forward" if self.slot.endswith("fwd") else "reversed"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Rendered:
    system: str
    user: str
    order: list[str]                 # product ids in shown order (position 1..8)
    scripted_reply: str              # what ask_user returns
    meta: dict = field(default_factory=dict)
    # V and M1V only: the reply to a second ask (depends on task and hidden need
    # only, never on the name). None in other arms, where a second ask ends the
    # episode as no purchase.
    followup_reply: str | None = None


class Catalog:
    def __init__(self, data_dir: Path = DATA):
        self.data_dir = Path(data_dir)
        tasks = json.loads((self.data_dir / "tasks.json").read_text())
        pages = json.loads((self.data_dir / "pages.json").read_text())
        products = json.loads((self.data_dir / "products.json").read_text())
        profiles = json.loads((self.data_dir / "profiles.json").read_text())
        self.meta = tasks["meta"]
        self.tasks = tasks["tasks"]
        self.task_by_id = {t["task_id"]: t for t in self.tasks}
        self.task_idx = {t["task_id"]: i for i, t in enumerate(self.tasks)}
        self.pages = {p["page_id"]: p for p in pages["pages"]}
        self.products = products["products"]
        self.profiles_all = profiles["profiles"]
        self.profile_by_id = {p["profile_id"]: p for p in self.profiles_all}
        self._parity_override: dict[str, int] = {}
        # Exploratory add-on profiles (PLAN D9). Kept out of profiles_all so every
        # main-run property (main_profiles, core_profiles, ...) is unchanged.
        addon = self.data_dir / "profiles_addon.json"
        self.addon_profiles = json.loads(addon.read_text())["profiles"] if addon.exists() else []
        for p in self.addon_profiles:
            assert p["profile_id"] not in self.profile_by_id, p["profile_id"]
            self.profile_by_id[p["profile_id"]] = p

    # ---------------- profiles ----------------
    @cached_property
    def main_profiles(self) -> list[dict]:
        return [p for p in self.profiles_all if p["role"] == "main"]

    @cached_property
    def core_profiles(self) -> list[dict]:
        return [p for p in self.main_profiles if p["tier"] == "core"]

    @cached_property
    def baseline_profiles(self) -> list[dict]:
        return [p for p in self.main_profiles if p["tier"] == "baseline"]

    def profile_ordinal(self, profile_id: str) -> int:
        """Index of the profile within its id prefix (BW01 -> 0, BASE3 -> 2)."""
        digits = "".join(ch for ch in profile_id if ch.isdigit())
        return int(digits) - 1

    def parity(self, profile_id: str) -> int:
        """Hidden-need parity. Alternates by ordinal within each identity cell
        (tasks.json meta.hidden_need_schedule). [Call] for alternates: an
        alternate that replaces a main name should take that name's parity;
        set it with set_parity() when that happens."""
        override = self._parity_override.get(profile_id)
        if override is not None:
            return override
        return self.profile_ordinal(profile_id) % 2

    def set_parity(self, profile_id: str, parity: int) -> None:
        self._parity_override[profile_id] = parity

    def hidden_need_for(self, task: dict, profile_id: str, slot: str) -> str:
        sched = self.meta["hidden_need_schedule"][f"names_parity_{self.parity(profile_id)}"]
        letter = sched[SLOT_TO_SCHEDULE[slot]]
        keys = list(task["hidden_needs"].keys())
        return keys[0] if letter == "A" else keys[1]

    # ---------------- episodes ----------------
    def make_episode(self, arm: str, profile_id: str, task_id: str, slot: str) -> Episode:
        task = self.task_by_id[task_id]
        base = BASE_ARM[arm]
        page_id = task["page_v"] if base == "V" else task["page_s"]
        need = self.hidden_need_for(task, profile_id, slot) if base == "V" else None
        tidx = self.task_idx[task_id]
        eid = f"{arm}_{profile_id}_{tidx:02d}_{slot}"
        return Episode(eid, arm, base, profile_id, task_id, tidx, slot, page_id, need)

    def render(self, ep: Episode) -> Rendered:
        task = self.task_by_id[ep.task_id]
        page = self.pages[ep.page_id]
        prof = self.profile_by_id[ep.profile_id]
        birth_year = prof["birth_year_by_run"][ep.slot]

        extra = prompts.M1_INSTRUCTION if ep.arm.startswith("M1") else ""
        system = prompts.SYSTEM_TEMPLATE.format(
            profile_lines=prompts.profile_lines(prof, birth_year, planted=(ep.arm == "PB")),
            extra=extra,
        )

        w = ep.wording
        if ep.base_arm == "V":
            request = task["request_vague"][w]
        else:
            request = task["request_specified"][w]
        if ep.arm in STATED_LINE:
            request = self.stated_request(task, STATED_LINE[ep.arm], w)
        if ep.base_arm == "S1":
            b = prompts.money(task["budget_s1"])
            request = request + " " + self.meta["s1_budget_sentence"][w].replace("${budget}", b)
        if ep.arm in prompts.P_SUFFIX:
            request = request + " " + prompts.P_SUFFIX[ep.arm]

        order = page["order_forward"] if ep.order == "forward" else page["order_reversed"]
        items = {it["product_id"]: it for it in page["items"]}
        blocks = []
        for pos, pid in enumerate(order, start=1):
            prod = dict(self.products[pid])
            prod["price"] = items[pid]["price"]  # page price is the frozen price
            blocks.append(prompts.render_product(pos, prod))
        user = prompts.USER_TEMPLATE.format(request=request, n=len(order), page="\n\n".join(blocks))

        followup = None
        if ep.base_arm == "V":
            reply = task["hidden_needs"][ep.hidden_need]
            followup = self.followup_reply(task, ep.hidden_need)
        else:
            reply = self.meta["arm_replies"]["S1" if ep.base_arm == "S1" else "S0"]

        return Rendered(system=system, user=user, order=list(order), scripted_reply=reply,
                        meta={"birth_year": birth_year, "request": request}, followup_reply=followup)

    @staticmethod
    def stated_request(task: dict, line: str, wording: int) -> str:
        """Add-on B: the S0 twin request with its "either line is fine" sentence
        replaced by one that states the line. Depends only on task, line and
        wording, never on the name."""
        base = task["request_specified"][wording]
        either = _EITHER[wording]
        assert task["group"] == "twin" and either in base, task["task_id"]
        return base.replace(either, f" I want the {_STATED_WORDS[line]} version.")

    def followup_reply(self, task: dict, hidden_need: str) -> str:
        """Reply to a second ask in V (deviation 11/4, PLAN.md). Takes only the
        task and the hidden need, so it cannot depend on the name."""
        tmpl = self.meta["v_followup_reply"]["template"]
        return tmpl.replace("{hidden_need_reply}", task["hidden_needs"][hidden_need])

    # ---------------- grids ----------------
    def _rng(self, purpose: str) -> random.Random:
        return random.Random(f"{SEED}-{purpose}")

    def planted_profiles(self) -> list[str]:
        """5 core Black names get the planted preference [Call]. A known gap
        on H1 (Black vs White, S0 price) that the frozen analysis must find."""
        black = [p["profile_id"] for p in self.core_profiles if p["race"] == "Black"]
        return sorted(self._rng("planted").sample(black, 5))

    def p_arm_selection(self) -> tuple[list[str], list[str]]:
        """Arm P: 20 tasks (stratified by group) x 16 core profiles (4 per cell)."""
        rng = self._rng("p_arm")
        quota = {"hair": 6, "skin": 4, "twin": 4, "neutral": 6}
        tasks = []
        for g, n in quota.items():
            ids = [t["task_id"] for t in self.tasks if t["group"] == g]
            tasks += sorted(rng.sample(ids, n), key=lambda x: self.task_idx[x])
        profs = []
        for cell in [("Black", "woman"), ("Black", "man"), ("White", "woman"), ("White", "man")]:
            ids = [p["profile_id"] for p in self.core_profiles if (p["race"], p["gender"]) == cell]
            profs += sorted(rng.sample(ids, 4))
        return tasks, profs

    def pilot_selection(self) -> tuple[list[str], list[str]]:
        """Pilot: 24 profiles (5 per core cell + 4 baseline) x 16 tasks."""
        rng = self._rng("pilot")
        quota = {"hair": 5, "skin": 3, "twin": 3, "neutral": 5}
        tasks = []
        for g, n in quota.items():
            ids = [t["task_id"] for t in self.tasks if t["group"] == g]
            tasks += sorted(rng.sample(ids, n), key=lambda x: self.task_idx[x])
        profs = []
        for cell in [("Black", "woman"), ("Black", "man"), ("White", "woman"), ("White", "man")]:
            ids = [p["profile_id"] for p in self.core_profiles if (p["race"], p["gender"]) == cell]
            profs += sorted(rng.sample(ids, 5))
        profs += [p["profile_id"] for p in self.baseline_profiles]
        return tasks, profs

    # ---------------- exploratory add-ons (PLAN D9) ----------------
    def addon_set(self, name_set: str) -> list[str]:
        """Profile ids an add-on preset runs: the set's main names, minus names
        listed in data/name_check_exclusions_addon.csv, each replaced in order by
        the next unused alternate of the same gender, which takes the dropped
        name's hidden-need parity (as PLAN 2 does for the main set)."""
        profs = [p for p in self.addon_profiles if p.get("set") == name_set]
        excl_path = self.data_dir / "name_check_exclusions_addon.csv"
        excluded: set[str] = set()
        if excl_path.exists():
            import csv
            excluded = {r["profile_id"] for r in csv.DictReader(open(excl_path))}
        out = []
        for gender in sorted({p["gender"] for p in profs}):
            mains = [p["profile_id"] for p in profs if p["gender"] == gender and p["role"] == "main"]
            alts = [p["profile_id"] for p in profs if p["gender"] == gender and p["role"] == "alternate"
                    and p["profile_id"] not in excluded]
            for pid in mains:
                if pid not in excluded:
                    out.append(pid)
                elif alts:
                    alt = alts.pop(0)
                    self.set_parity(alt, self.parity(pid))
                    out.append(alt)
        return out

    def _one_slot(self, profile_id: str, rank: int) -> str:
        """Single-run designs rotate the slot across the design's tasks (rank =
        position in its task list) so each name sees every wording, order and
        (in V) both needs equally often."""
        k = rank + self.profile_ordinal(profile_id)
        return SLOTS[k % 4]

    def _slot_pair(self, profile_id: str, task_id: str) -> tuple[str, str]:
        k = self.task_idx[task_id] + self.profile_ordinal(profile_id)
        return SLOT_PAIRS[k % 2]

    def grid(self, preset: str) -> list[Episode]:
        """Return the episodes of a named design, in a fixed (unshuffled) order."""
        eps: list[Episode] = []
        all_tasks = [t["task_id"] for t in self.tasks]
        if preset == "main":
            for p in self.main_profiles:
                for t in all_tasks:
                    for arm in ("S0", "S1", "V"):
                        for s in SLOTS:
                            eps.append(self.make_episode(arm, p["profile_id"], t, s))
        elif preset == "planted":
            for pid in self.planted_profiles():
                for t in all_tasks:
                    for s in SLOTS:
                        eps.append(self.make_episode("PB", pid, t, s))
        elif preset == "validity":
            tasks, profs = self.p_arm_selection()
            for pid in profs:
                for rank, t in enumerate(tasks):
                    s = self._one_slot(pid, rank)
                    for arm in ("PC", "PQ"):
                        eps.append(self.make_episode(arm, pid, t, s))
        elif preset in ("m1", "reduced"):
            arms = ("M1S0", "M1V") if preset == "m1" else ("S0", "V")
            profs = [p["profile_id"] for p in self.core_profiles + self.baseline_profiles]
            for pid in profs:
                for t in all_tasks:
                    for s in self._slot_pair(pid, t):
                        for arm in arms:
                            eps.append(self.make_episode(arm, pid, t, s))
        elif preset == "olmo":
            profs = [p["profile_id"] for p in self.core_profiles + self.baseline_profiles]
            for pid in profs:
                for rank, t in enumerate(all_tasks):
                    s = self._one_slot(pid, rank)
                    for arm in ("S0", "S1", "V"):
                        eps.append(self.make_episode(arm, pid, t, s))
        elif preset == "pilot":
            tasks, profs = self.pilot_selection()
            for pid in profs:
                for rank, t in enumerate(tasks):
                    s = self._one_slot(pid, rank)
                    for arm in ("S0", "S1", "V"):
                        eps.append(self.make_episode(arm, pid, t, s))
        elif preset == "pilotsmall":
            # About 160 episodes per model (11/4 pilot, PILOT_REPORT.md). The 24 pilot
            # profiles each run 6 fixed task/arm/slot cells, so every cell holds all
            # 20 core names and the cell-mean removal in analyze.py keeps real
            # variation. Plus PB for the 5 planted names on the two S0 cells, and S0 on
            # those cells for planted names outside the pilot set (so PB - S0 pairs).
            _, profs = self.pilot_selection()
            for pid in profs:
                for arm, t, s in PILOTSMALL_CELLS:
                    eps.append(self.make_episode(arm, pid, t, s))
            s0_cells = [(t, s) for arm, t, s in PILOTSMALL_CELLS if arm == "S0"]
            for pid in self.planted_profiles():
                for t, s in s0_cells:
                    eps.append(self.make_episode("PB", pid, t, s))
                    if pid not in profs:
                        eps.append(self.make_episode("S0", pid, t, s))
        elif preset == "vfollowup":
            # Check of the V follow-up reply (deviation 11/4, PLAN.md): the exact V
            # episodes of the pilot preset (same names, tasks, slots and needs) on
            # the 6 pilot tasks with the most second asks, so before and after
            # compare episode by episode. 24 profiles x 6 tasks = 144 episodes.
            tasks, profs = self.pilot_selection()
            for pid in profs:
                for rank, t in enumerate(tasks):
                    if t in VFOLLOWUP_TASKS:
                        eps.append(self.make_episode("V", pid, t, self._one_slot(pid, rank)))
        elif preset in ("neutral", "arab", "sasian"):
            # Add-ons A and C (PLAN D9): S0 and V, all 4 slots, like the main grid.
            # A runs the 8 twin tasks only; C runs all 40 tasks (extended-tier shape).
            tasks = [t["task_id"] for t in self.tasks if t["group"] == "twin"] if preset == "neutral" else all_tasks
            for pid in self.addon_set(preset):
                for t in tasks:
                    for arm in ("S0", "V"):
                        for s in SLOTS:
                            eps.append(self.make_episode(arm, pid, t, s))
        elif preset == "stated":
            # Add-on B (PLAN D9): the 40 core names x 8 twin tasks x both stated lines x 4 slots.
            twins = [t["task_id"] for t in self.tasks if t["group"] == "twin"]
            for p in self.core_profiles:
                for t in twins:
                    for arm in ("STM", "STW"):
                        for s in SLOTS:
                            eps.append(self.make_episode(arm, p["profile_id"], t, s))
        else:
            raise ValueError(f"unknown preset {preset!r}")
        return eps

    @staticmethod
    def interleave(eps: list[Episode], seed_label: str) -> list[Episode]:
        """Shuffle so names, arms and tasks are mixed within every batch and
        across time (design 5.5 run hygiene)."""
        out = list(eps)
        random.Random(f"{SEED}-interleave-{seed_label}").shuffle(out)
        return out


PRESETS = ["main", "planted", "validity", "m1", "reduced", "olmo", "pilot", "pilotsmall", "vfollowup",
           "neutral", "stated", "arab", "sasian"]   # last four: exploratory add-ons, PLAN D9

# vfollowup: the 6 pilot V tasks with the most second asks in pilot_haiku
# (11/4), chosen to stress the fix. Not a confirmatory design.
VFOLLOWUP_TASKS = ("hair_mask_coily_4c", "skin_concealer_deep_shade", "skin_tint_deep_shade",
                   "twin_razor", "twin_body_wash", "neutral_toaster")

# pilotsmall: (arm, task, slot). One slot per task, all 4 wording x order slots used.
# S0: one hair task and one neutral task (H1, H2). S1: one hair and one skin task
# (with the S0 hair task, H3). V: one hair and one skin task (H4); the hidden need
# follows name parity, so half the names in each cell get each need.
PILOTSMALL_CELLS = [
    ("S0", "hair_shampoo_coily_4c", "w1_fwd"),
    ("S0", "neutral_mouse", "w2_rev"),
    ("S1", "hair_mask_fine_straight", "w1_rev"),
    ("S1", "skin_tint_deep_shade", "w2_fwd"),
    ("V", "hair_mask_coily_4c", "w2_rev"),
    ("V", "skin_concealer_deep_shade", "w1_rev"),
]
