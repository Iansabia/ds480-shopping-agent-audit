"""Build every journal-style paper figure: imports each module and calls make().

Run: "<repo>/.venv/bin/python" analysis/paperfigs/build_all.py
Output: paper/figures/paper/<figname>.pdf and .png
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

FIGS = ["fig1_summary_card", "fig3_race_groups", "fig4_price_gap", "fig5_method_checks",
        "fig6_hair_skin_fit", "fig7_ask_rates", "fig8_name_blind", "figA1_position_bias",
        "figA2_price_vs_no_name", "figA3_training_data_link", "figA4_model_scorecard",
        "figA5_random_split", "figA6_gender_line", "figA7_race_groups", "figA8_dollars_by_cell"]


def main(names=None):
    out = []
    for n in names or FIGS:
        out.append(importlib.import_module(f"paperfigs.{n}").make())
        print(out[-1])
    return out


if __name__ == "__main__":
    main(sys.argv[1:] or None)
