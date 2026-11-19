#!/usr/bin/env python3
"""Build labelled contact sheets (desktop+mobile thumbnails) for visual review."""
import json, os, sys, re
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from build_crm import norm_dom
rows = json.load(open("data/crm_leads.json")); aud = json.load(open("data/audits.json"))
done = set(json.load(open("data/visual.json")).keys()) if os.path.exists("data/visual.json") else set()
items = []
for r in rows:
    d = norm_dom(r["web_sitesi"]); a = aud.get(d)
    if not a or not a.get("reachable") or r["key"] in done: continue
    name = a["final_url"].replace("https://", "").replace("http://", "")
    name = re.sub(r"[^a-z0-9.]", "_", name, flags=re.I)[:60]
    dp, mp = f"data/shots/{name}_d.jpg", f"data/shots/{name}_m.jpg"
    if os.path.exists(dp) and os.path.exists(mp):
        items.append((r, dp, mp))
os.makedirs("data/sheets", exist_ok=True)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
except Exception:
    font = ImageFont.load_default()
W, H = 560, 369  # desktop thumb
MW, MH = 170, 369
per = 6
idx = []
for s in range(0, len(items), per):
    chunk = items[s:s + per]
    sheet = Image.new("RGB", (2 * (W + MW + 20), 3 * (H + 30)), "white")
    dr = ImageDraw.Draw(sheet)
    for j, (r, dp, mp) in enumerate(chunk):
        x = (j % 2) * (W + MW + 20); y = (j // 2) * (H + 30)
        dr.text((x + 4, y + 4), f"{r['lead_id']} {r['firma_adi'][:38]}", fill="black", font=font)
        sheet.paste(Image.open(dp).resize((W, H)), (x, y + 28))
        m = Image.open(mp); m = m.resize((MW, int(MW * m.height / m.width)))
        sheet.paste(m.crop((0, 0, MW, MH)), (x + W + 5, y + 28))
        idx.append((s // per, r["lead_id"], r["key"]))
    sheet.save(f"data/sheets/sheet_{s // per:02d}.jpg", quality=60)
json.dump(idx, open("data/sheets/index.json", "w"))
print(len(items), "sites,", (len(items) + per - 1) // per, "sheets")
