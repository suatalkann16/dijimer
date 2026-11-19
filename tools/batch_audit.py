#!/usr/bin/env python3
"""Audit many URLs in parallel; merges into data/audits.json keyed by normalized domain."""
import json, sys, os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
sys.path.insert(0, os.path.dirname(__file__))
from site_audit import audit
def dom(u):
    u=u if u.startswith("http") else "http://"+u
    return urlparse(u).netloc.lower().replace("www.","")
path="data/audits.json"
db=json.load(open(path)) if os.path.exists(path) else {}
urls=[l.strip() for l in open(sys.argv[1]) if l.strip()]
todo=[u for u in urls if dom(u) not in db or "--force" in sys.argv]
def run(u):
    try: return u, audit(u)
    except Exception as e: return u, {"input":u,"reachable":False,"error":str(e)[:100]}
with ThreadPoolExecutor(8) as ex:
    for u,r in ex.map(run,todo):
        db[dom(u)]=r
        print(dom(u), r.get("reachable"), r.get("status"), file=sys.stderr)
json.dump(db,open(path,"w"),ensure_ascii=False,indent=1)
print(len(db),"audited")
