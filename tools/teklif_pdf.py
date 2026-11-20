#!/usr/bin/env python3
"""Dijimer teklif Markdown -> A4 PDF (kurumsal renkler, logo, sayfa numarası).

Kullanım: python3 tools/teklif_pdf.py musteriler/<firma>/teklif-<no>.md [cikti.pdf]
Gerekenler: pip install markdown · Playwright (Chromium) ortamda kurulu.
"""
import os, re, subprocess, sys, tempfile, urllib.request
import markdown

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".pdf"
md = open(src, encoding="utf-8").read()
md = re.sub(r"<!--.*?-->", "", md, flags=re.S)  # yönergeleri PDF'e taşıma

# Markdown içindeki <div> bloklarının içi de işlensin
html_body = markdown.markdown(md, extensions=["tables", "sane_lists", "md_in_html", "attr_list"])
html_body = html_body.replace('<div class="page-break"></div>', '<div style="page-break-after:always"></div>')
html_body = re.sub(r"\[ \]", "&#9744;", html_body)  # onay kutuları

# Logo: sitedeki SVG; erişilemezse metin logo kalır
logo = ""
try:
    logo = urllib.request.urlopen("https://dijimerbilisim.com/images/marka/dijimer-logo.svg", timeout=10).read().decode()
except Exception:
    pass
if logo:
    html_body = html_body.replace('<div class="kapak-logo">DİJİMER BİLİŞİM</div>',
                                  f'<div class="kapak-logo svg">{logo}</div>', 1)

leftover = sorted(set(re.findall(r"\[[A-ZÇĞİÖŞÜ0-9][^\]]{1,80}\]", md)))

css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
:root { --red:#E53935; --ink:#0F1115; --text:#3F444B; --muted:#5B616B; --blue:#1F5F8B; --blue-soft:#E7F0F7; --border:#E6E7EA; --surface:#F7F7F8; }
body { font-family:'Plus Jakarta Sans','DejaVu Sans',Arial,sans-serif; color:var(--text); font-size:10.5pt; line-height:1.5; }
h1,h2,h3,h4 { color:var(--ink); line-height:1.25; }
h2 { font-size:15pt; margin:22px 0 8px; padding-bottom:6px; border-bottom:2px solid var(--red); }
h3 { font-size:12pt; margin:16px 0 6px; color:var(--blue); }
h4 { font-size:11pt; margin:14px 0 4px; }
a { color:var(--blue); text-decoration:none; }
hr { border:0; border-top:1px solid var(--border); margin:18px 0; }
table { width:100%; border-collapse:collapse; margin:8px 0 12px; page-break-inside:avoid; }
th { background:var(--ink); color:#fff; text-align:left; font-weight:600; padding:7px 9px; font-size:9.5pt; }
td { padding:7px 9px; border-bottom:1px solid var(--border); vertical-align:top; font-size:9.8pt; }
tr:nth-child(even) td { background:var(--surface); }
td strong { color:var(--ink); }
ul { padding-left:18px; } li { margin:3px 0; }
.kapak { min-height:240mm; display:flex; flex-direction:column; justify-content:center; }
.kapak-logo { font-weight:800; font-size:22pt; color:var(--red); letter-spacing:1px; }
.kapak-logo.svg svg { width:62mm; height:auto; }
.kapak-alt { color:var(--muted); margin:4px 0 40px; font-weight:600; }
.kapak h1 { font-size:34pt; margin:0; border:0; color:var(--ink); }
.kapak h2 { font-size:17pt; border:0; color:var(--red); margin:6px 0 28px; }
.kapak table th { display:none; }
.kapak table td { background:#fff !important; border-bottom:1px solid var(--border); font-size:11pt; }
.kapak table td:first-child { width:38%; color:var(--muted); }
.iletisim { background:var(--blue-soft); border-left:4px solid var(--red); padding:12px 16px; }
"""
footer = ('<div style="font-family:Arial;font-size:7.5pt;color:#5B616B;width:100%;padding:0 16mm;display:flex;justify-content:space-between">'
          '<span>Dijimer Bilişim · 0538 370 11 79 · info@dijimerbilisim.com · dijimerbilisim.com</span>'
          '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
html = f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{css}</style></head><body>{html_body}</body></html>'

with tempfile.TemporaryDirectory() as d:
    hp = os.path.join(d, "t.html"); open(hp, "w", encoding="utf-8").write(html)
    js = f"""
const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}',{{waitUntil:'networkidle'}}).catch(()=>{{}});
await p.pdf({{path:{out!r},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
footerTemplate:{footer!r},margin:{{top:'18mm',bottom:'20mm',left:'16mm',right:'16mm'}}}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)

print("PDF:", out)
if leftover:
    print(f"UYARI: Doldurulmamış {len(leftover)} yer tutucu var:", ", ".join(leftover[:15]), "…" if len(leftover) > 15 else "")
