#!/usr/bin/env python3
"""Crawl kurumsal.web.tr 'Arıtma' sector listing + detail pages -> data/raw_kurumsal.json"""
import json, re, time, requests, sys
from bs4 import BeautifulSoup
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
S=requests.Session(); S.headers["User-Agent"]=UA
def cf(h):
    k=int(h[:2],16); return "".join(chr(int(h[i:i+2],16)^k) for i in range(2,len(h),2))
base=sys.argv[1] if len(sys.argv)>1 else "https://www.kurumsal.web.tr/sektor/aritma/"
links=[]
for p in range(1,30):
    u=base+(f"?sayfa={p}" if p>1 else "")
    s=BeautifulSoup(S.get(u,timeout=25).content,"lxml")
    new=[a["href"] for a in s.find_all("a",href=True) if "/firma/" in a["href"]]
    new=[n if n.startswith("http") else "https://www.kurumsal.web.tr"+n for n in new]
    new=[n for n in new if n not in links]
    if not new: break
    links+=new; time.sleep(3)
print(len(links),"detail links",file=sys.stderr)
out=[]
for l in links:
    s=None
    for attempt in range(4):
        try:
            resp=S.get(l,timeout=25)
        except Exception:
            time.sleep(10); continue
        if resp.status_code==429 or b"error-1015" in resp.content or resp.status_code>=500:
            time.sleep(60); continue
        s=BeautifulSoup(resp.content,"lxml"); break
    if s is None: continue
    d={"src":l}
    for el in s.select("[data-cfemail]"):
        d.setdefault("emails",[]).append(cf(el["data-cfemail"]))
    for a in s.find_all("a",href=True):
        if "/cdn-cgi/l/email-protection#" in a["href"]:
            d.setdefault("emails",[]).append(cf(a["href"].split("#")[1]))
    t=s.get_text(" | ",strip=True)
    def grab(lbl,nxt):
        m=re.search(re.escape(lbl)+r" \| (.*?) \| (?:"+nxt+")",t)
        return m.group(1) if m else ""
    d["name"]=grab("Firma Ünvanı","Açıklama")
    d["desc"]=grab("Açıklama","Web Adresi|Telefon|Adres|E-posta")[:500]
    ext=[a["href"] for a in s.find_all("a",href=True) if a["href"].startswith("http") and "kurumsal.web.tr" not in a["href"] and "cdn-cgi" not in a["href"]]
    d["web"]=ext[0] if ext else ""
    m=re.search(r"Telefon \| (.*?) \|",t); d["phone"]=m.group(1) if m else ""
    m=re.search(r"Adres \| (.*?) \| Hizmet",t); d["address"]=m.group(1) if m else ""
    m=re.search(r"Hizmet verdiği şehirler \| (.*?) \| Bilgileri",t); d["cities"]=m.group(1) if m else ""
    d["emails"]=sorted(set(d.get("emails",[])))
    out.append(d); time.sleep(3)
json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else "data/raw_kurumsal.json","w"),ensure_ascii=False,indent=1)
print(len(out),file=sys.stderr)
