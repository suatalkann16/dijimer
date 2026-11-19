#!/usr/bin/env python3
"""Fetch home + about/references/contact/projects pages for a domain; save plain text for research."""
import sys, os, re, json, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
sys.path.insert(0, os.path.dirname(__file__))
from site_audit import get
KEYS = ("hakk", "kurumsal", "about", "referans", "proje", "iletisim", "iletişim", "contact", "faaliyet", "hizmet", "uretim", "üretim", "tesis")
def text(html):
    s = BeautifulSoup(html, "lxml")
    for x in s(["script", "style", "noscript", "svg"]): x.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ", strip=True))
for dom in sys.argv[1:]:
    out = f"data/pages/{dom}.txt"
    os.makedirs("data/pages", exist_ok=True)
    try:
        r = get("https://" + dom)
    except Exception as e:
        try: r = get("https://www." + dom)
        except Exception as e2:
            print(dom, "ERR"); continue
    soup = BeautifulSoup(r.text, "lxml")
    base = urlparse(r.url).netloc
    links = []
    for a in soup.find_all("a", href=True):
        h = urljoin(r.url, a["href"]); t = (a.get_text(" ", strip=True) + " " + h).lower()
        if urlparse(h).netloc == base and any(k in t for k in KEYS) and h not in links and "#" not in h[-2:]:
            links.append(h)
    buf = [f"=== HOME {r.url}\n{text(r.text)[:3000]}"]
    for h in links[:7]:
        try:
            p = get(h, timeout=15); buf.append(f"=== {h}\n{text(p.text)[:2500]}")
        except Exception: pass
    open(out, "w").write("\n\n".join(buf)); print(dom, len(links), "pages")
