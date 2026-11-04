"""Read Gaddis (2017) Table 1 font styles: bold = lowest quartile of mother's education
within race, italic = highest quartile, regular = middle two quartiles.
Run: .venv/bin/python -I src/gaddis_table1_fonts.py <pdf> <out.csv>"""
import sys, collections
import pdfplumber, pandas as pd
p = pdfplumber.open(sys.argv[1]).pages[6]
ch = [c for c in p.chars if not c["upright"]]
cols = collections.defaultdict(list)
for c in ch:
    cols[round(c["x0"], 0)].append(c)
words = []
for x, cs in cols.items():
    cs.sort(key=lambda c: -c["top"])  # rotated text: try both directions below
    cur = [cs[0]]
    for a, b in zip(cs, cs[1:]):
        if abs(a["top"] - b["top"]) > 12 or b["fontname"] != a["fontname"]:
            words.append(cur); cur = [b]
        else:
            cur.append(b)
    words.append(cur)
rows = []
for w in words:
    t1 = "".join(c["text"] for c in w)
    t2 = t1[::-1]
    font = w[0]["fontname"]
    style = "bold" if "Bold" in font else "italic" if "Ital" in font else "regular"
    rows.append({"text_a": t1, "text_b": t2, "style": style, "x": w[0]["x0"], "top": w[0]["top"]})
df = pd.DataFrame(rows)
df.to_csv(sys.argv[2], index=False)
print(df.to_string())
