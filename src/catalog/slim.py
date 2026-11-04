"""Stream Amazon Reviews 2023 metadata files and keep a slim candidate pool.

Keeps only items with a numeric price, a rating, and at least MIN_RATINGS ratings.
Output: data/raw/slim/<category>.jsonl (git-ignored).
"""
import gzip, json, sys, os

MIN_RATINGS = 30

def open_any(p):
    if p == "-":
        return sys.stdin
    return gzip.open(p, "rt") if p.endswith(".gz") else open(p, "rt")

def to_price(v):
    if v is None:
        return None
    try:
        x = float(str(v).replace("$", "").replace(",", "").strip())
        return x if 0.5 <= x <= 2000 else None
    except ValueError:
        return None

def main(src, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    n = kept = 0
    with open_any(src) as f, open(out, "w") as g:
        for line in f:
            n += 1
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            price = to_price(d.get("price"))
            rn = d.get("rating_number") or 0
            if price is None or rn < MIN_RATINGS or not d.get("title"):
                continue
            det = d.get("details") or {}
            slim = {
                "asin": d.get("parent_asin"),
                "title": d["title"][:300],
                "store": d.get("store"),
                "price": price,
                "rating": d.get("average_rating"),
                "rating_number": rn,
                "main_category": d.get("main_category"),
                "categories": d.get("categories") or [],
                "features": [str(x)[:200] for x in (d.get("features") or [])[:5]],
                "details": {k: str(v)[:100] for k, v in det.items() if k in (
                    "Brand", "Hair Type", "Skin Type", "Color", "Item Form", "Scent", "Size",
                    "Material", "Product Benefits", "Special Feature", "Connectivity Technology",
                    "Capacity", "Target Gender", "Recommended Uses For Product", "Skin Tone",
                    "Finish Type", "Coverage", "Number of Blades", "Date First Available")},
            }
            g.write(json.dumps(slim) + "\n")
            kept += 1
    print(f"{src}: read {n}, kept {kept}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
