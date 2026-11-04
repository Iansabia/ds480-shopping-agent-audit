"""Print every page compactly for manual label review."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "data/pages.json")))["pages"]
pr = json.load(open(os.path.join(ROOT, "data/products.json")))["products"]
filt = sys.argv[1] if len(sys.argv) > 1 else ""
for p in P:
    if filt not in p["page_id"]:
        continue
    print(f"== {p['page_id']}  budget={p.get('budget_s1')}")
    for it in p["items"]:
        x = pr[it["product_id"]]
        print(f"  {it['slot']:<16} {it.get('need_line',''):<14} ${it['price']:>7.2f} {x['rating']} {it['product_id']} | {x['title'][:105]}")
