#!/usr/bin/env python3
"""Fetch a URL and print visible text + outbound links (for directory pages)."""
import sys, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
u=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 6000
r=requests.get(u,headers={"User-Agent":UA},timeout=25)
r.encoding = r.apparent_encoding if r.encoding in (None,'ISO-8859-1') else r.encoding
s=BeautifulSoup(r.text,"lxml")
for x in s(["script","style","noscript"]): x.decompose()
print("STATUS",r.status_code,r.url)
print(s.get_text(" | ",strip=True)[:n])
if "--links" in sys.argv:
    seen=set()
    for a in s.find_all("a"):
        h=urljoin(r.url,a.get("href") or "")
        if h not in seen: seen.add(h); print("L",h,"|",a.get_text(" ",strip=True)[:60])
