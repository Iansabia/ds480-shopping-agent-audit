"""List each unique (product, label) once, grouped by product type and line, for manual review."""
import json, os, sys
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "data/pages.json")))["pages"]
T = {t["task_id"]: t for t in json.load(open(os.path.join(ROOT, "data/tasks.json")))["tasks"]}
pr = json.load(open(os.path.join(ROOT, "data/products.json")))["products"]
filt = sys.argv[1] if len(sys.argv) > 1 else ""
g = defaultdict(dict)
for p in P:
    t = T[p["task_id"]]
    if filt not in p["task_id"]:
        continue
    for it in p["items"]:
        kind = "NM" if it["slot"] == "near_miss" else "FIT"
        g[(t["group"], t["product_type"], kind, it.get("need_line"))][it["product_id"]] = it["price"]
for k in sorted(g):
    print("==", *k)
    for pid, price in sorted(g[k].items(), key=lambda x: x[1]):
        x = pr[pid]
        print(f"  ${price:>7.2f} {x['rating']} {pid} | {x['title'][:120]}")
