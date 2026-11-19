import json,os,sys
idx={lid:key for _,lid,key in json.load(open('data/sheets/index.json'))}
v=json.load(open('data/visual.json')) if os.path.exists('data/visual.json') else {}
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    lid,g,n=line.split('|',2)
    v[idx[lid.strip()]]={"grade":int(g),"note":n.strip(),"lead_id":lid.strip()}
json.dump(v,open('data/visual.json','w'),ensure_ascii=False,indent=1); print(len(v))
