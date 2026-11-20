#!/usr/bin/env python3
"""Merge lead sources -> dedupe -> audit lookup -> score -> data/crm_leads.json + CSV.

Inputs
  data/seeds_search.tsv     leads found via web search (name, city, url, subsector, source)
  data/raw_kurumsal.json    kurumsal.web.tr 'Arıtma' sector directory crawl
  data/audits.json          technical website audits (tools/batch_audit.py)
  data/manual.json          manual research notes / overrides per lead key (optional)
Output
  data/crm_leads.json, data/crm_leads.csv
"""
import csv, json, os, re, sys, unicodedata
from urllib.parse import urlparse
sys.path.insert(0, os.path.dirname(__file__))
from score import website_score, potential

TODAY = "2026-11-19"
CITIES = ["Bursa", "İstanbul", "Kocaeli", "İzmir", "Ankara", "Balıkesir", "Sakarya", "Eskişehir", "Tekirdağ",
          "Manisa", "Denizli", "Konya", "Kayseri", "Gaziantep", "Adana", "Antalya", "Mersin", "Samsun", "Trabzon",
          "Zonguldak", "Düzce", "Yalova", "Bolu", "Kütahya", "Aydın", "Muğla", "Hatay", "Malatya", "Diyarbakır",
          "Erzurum", "Kahramanmaraş", "Çorum", "Uşak", "Afyon", "Bilecik", "Edirne", "Kırklareli", "Çanakkale"]
FREE_MAIL = ("gmail.", "hotmail.", "outlook.", "yahoo.", "yandex.", "icloud.", "mynet.", "windowslive.", "live.")


def norm_dom(u):
    if not u:
        return ""
    u = u.strip()
    if not u.startswith("http"):
        u = "http://" + u
    d = urlparse(u).netloc.lower().replace("www.", "")
    return d if "." in d and "@" not in d else ""


def norm_name(n):
    n = unicodedata.normalize("NFKD", n.lower().replace("ı", "i")).encode("ascii", "ignore").decode()
    n = re.sub(r"\b(ltd|sti|san|tic|ve|as|a\.s|ins|muh|muhendislik|sanayi|ticaret|limited|sirketi|arıtma|aritma|sistemleri|cevre|teknolojileri|su)\b", " ", n)
    return re.sub(r"[^a-z0-9]", "", n)


def city_of(text):
    t = text or ""
    for c in CITIES:
        if c.lower() in t.lower() or c.upper() in t:
            return c
    tt = t.replace("İ", "I").lower()
    for c in CITIES:
        if c.replace("İ", "I").lower() in tt:
            return c
    return ""


AREA = {"224": "Bursa", "212": "İstanbul", "216": "İstanbul", "262": "Kocaeli", "232": "İzmir", "312": "Ankara",
        "266": "Balıkesir", "264": "Sakarya", "222": "Eskişehir", "282": "Tekirdağ", "236": "Manisa", "258": "Denizli",
        "332": "Konya", "352": "Kayseri", "342": "Gaziantep", "322": "Adana", "242": "Antalya", "324": "Mersin",
        "362": "Samsun", "462": "Trabzon", "422": "Malatya", "344": "Kahramanmaraş", "272": "Afyon", "276": "Uşak",
        "256": "Aydın", "252": "Muğla", "226": "Yalova", "380": "Düzce", "286": "Çanakkale", "284": "Edirne", "228": "Bilecik"}


def city_from_phone(*phones):
    for ph in phones:
        d = re.sub(r"\D", "", ph or "")
        d = d[2:] if d.startswith("90") else d
        d = d[1:] if d.startswith("0") else d
        if d[:3] in AREA:
            return AREA[d[:3]]
    return ""


def district_of(addr, city):
    m = re.search(r"([A-ZÇĞİÖŞÜa-zçğıöşü]+)\s*/\s*" + (city.upper() if city else "[A-ZÇĞİÖŞÜ]+"), addr or "")
    return m.group(1).title() if m else ""


def load():
    leads = []
    with open("data/seeds_search.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            leads.append({"name": row["name"], "city": row["city"].replace("?", ""), "web": row["url"],
                          "subsector": row["subsector"], "sources": [row["source"]], "desc": "", "phone": "", "address": "",
                          "dir_emails": []})
    if os.path.exists("data/raw_kurumsal.json"):
        for d in json.load(open("data/raw_kurumsal.json")):
            if not d.get("name"):
                continue
            web = d.get("web", "")
            if "@" in web:  # e-mail typed into URL field -> treat as e-mail, no website
                d.setdefault("emails", []).append(web.split("//")[-1])
                web = ""
            if any(x in web for x in ("cloudflare.com", "kurumsal.web.tr", "facebook.com", "instagram.com")):
                web = ""
            sc = [c.strip() for c in d.get("cities", "").split("|") if c.strip()]
            city = city_of(d.get("address", "")) or city_from_phone(d.get("phone", "")) or (city_of(sc[0]) if 0 < len(sc) <= 3 else "")
            leads.append({"name": d["name"].strip(), "city": city, "web": web, "subsector": "", "sources": [d["src"]],
                          "desc": d.get("desc", ""), "phone": d.get("phone", ""), "address": d.get("address", ""),
                          "dir_emails": [e.replace("www.", "", 1) if e.startswith("www.") else e for e in d.get("emails", [])],
                          "served_cities": d.get("cities", "")})
    return leads


def dedupe(leads):
    out = {}
    for l in leads:
        dom = norm_dom(l["web"])
        key = dom or norm_name(l["name"])
        alt = norm_name(l["name"])
        hit = out.get(key)
        if not hit:
            for k, v in out.items():
                if alt and (norm_name(v["name"]) == alt):
                    hit = v; break
        if hit:
            for f in ("city", "web", "subsector", "desc", "phone", "address", "served_cities"):
                if not hit.get(f) and l.get(f):
                    hit[f] = l[f]
            hit["sources"] = list(dict.fromkeys(hit["sources"] + l["sources"]))
            hit["dir_emails"] = sorted(set(hit["dir_emails"]) | set(l["dir_emails"]))
        else:
            l["key"] = key
            out[key] = l
    return list(out.values())


def pick_email(l, a):
    dom = norm_dom(l["web"])
    site_em = (a or {}).get("emails", []) if a and a.get("reachable") else []
    on_dom = [e for e in site_em if dom and e.split("@")[1].endswith(dom.split(":")[0])]
    pref = ("info", "iletisim", "bilgi", "satis", "sales", "contact", "teklif", "proje")
    def rank(e):
        u = e.split("@")[0]
        return next((i for i, p in enumerate(pref) if u.startswith(p)), 99)
    if on_dom:
        e = sorted(on_dom, key=rank)[0]
        return e, "Doğrulanmış – resmi web sitesi", l["web"]
    base = dom.split(".")[0] if dom else ""
    same_brand = [e for e in site_em if base and e.split("@")[1].split(".")[0] == base]
    if same_brand:  # e.g. site agtsuaritma.com.tr, mail @agtsuaritma.com
        e = sorted(same_brand, key=rank)[0]
        return e, "Doğrulanmış – resmi web sitesi (aynı marka, farklı uzantı)", l["web"]
    def looks_like_company(e):
        u = re.sub(r"[^a-z]", "", e.split("@")[0].lower())
        b = re.sub(r"[^a-z]", "", base)
        return bool(b) and (u[:4] in b or b[:4] in u)
    free = [e for e in site_em if any(f in e.split("@")[1] for f in FREE_MAIL) and looks_like_company(e)]
    if free:
        e = sorted(free, key=rank)[0]
        return e, "Doğrulanmış – resmi web sitesi (ücretsiz e-posta servisi)", l["web"]
    other = [e for e in site_em if e not in free]
    if other:
        # address on a different domain (could be agency/theme author or sister company) -> not send-ready
        e = sorted(other, key=rank)[0]
        return e, "Tahmini – doğrulanmadı (sitede farklı alan adlı adres)", l["web"]
    if l["dir_emails"]:
        e = sorted(l["dir_emails"], key=rank)[0]
        return e, "Güvenilir kaynak", l["sources"][0]
    return "", "Bulunamadı", ""


def main():
    audits = json.load(open("data/audits.json")) if os.path.exists("data/audits.json") else {}
    manual = json.load(open("data/manual.json")) if os.path.exists("data/manual.json") else {}
    visual = json.load(open("data/visual.json")) if os.path.exists("data/visual.json") else {}
    autosub = json.load(open("data/auto_sub.json")) if os.path.exists("data/auto_sub.json") else {}
    leads = dedupe(load())
    rows = []
    for i, l in enumerate(sorted(leads, key=lambda x: (x["city"] != "Bursa", x["name"]))):
        dom = norm_dom(l["web"])
        a = audits.get(dom) if dom else None
        mo = manual.get(l["key"], {})
        for f, v in mo.items():
            if f in ("name", "city", "district", "subsector", "address", "phone", "web", "linkedin", "instagram", "owner"):
                l[f] = v
        email, est, esrc = pick_email(l, a)
        if mo.get("email"):
            email, est, esrc = mo["email"], mo.get("email_status", "Güvenilir kaynak"), mo.get("email_source", "")
        if not l["city"] and a and a.get("reachable"):
            l["city"] = city_from_phone(*a.get("phones", [])) or city_of(a.get("contact_text", ""))
        if not l.get("phone") and a and a.get("phones"):
            l["phone"] = a["phones"][0]
        if not dom and not mo.get("no_site_verified"):
            wst = "A?"
        vis = visual.get(l["key"])
        ws, wbr, wstat = website_score(a if dom else None, vis)
        if not l.get("subsector"):
            l["subsector"] = autosub.get(l["key"], "")
        if not dom:
            wstat = "A" if mo.get("no_site_verified") else "A?"
        if mo.get("web_status"):
            wstat = mo["web_status"]
        l.update(email=email, email_status=est, size_adj=mo.get("size_adj", 0), comm_adj=mo.get("comm_adj", 0))
        ps, pbr, cat = potential(l, a, ws, "A" if wstat.startswith("A") else wstat, vis)
        if mo.get("exclude"):
            cat = "C"
        if mo.get("cat_cap") and ["A+", "A", "B", "C"].index(cat) < ["A+", "A", "B", "C"].index(mo["cat_cap"]):
            cat = mo["cat_cap"]  # e.g. A+ requires verified contact; capped with reason in notes
        social = (a or {}).get("social", {})
        rows.append({
            "lead_id": f"DJ-ENV-{i+1:03d}",
            "key": l["key"],
            "firma_adi": l["name"],
            "sektor": "Çevre teknolojileri / Su ve atıksu arıtma",
            "alt_sektor": l.get("subsector") or mo.get("subsector", ""),
            "sehir": l["city"],
            "ilce": l.get("district") or district_of(l.get("address", ""), l["city"]),
            "adres": l.get("address", ""),
            "telefon": l.get("phone", ""),
            "eposta": email,
            "eposta_durumu": est,
            "eposta_kaynagi": esrc,
            "web_sitesi": l["web"],
            "web_durumu": {"A": "A – Web sitesi yok", "A?": "A? – Web sitesi bulunamadı (doğrulanacak)", "B": "B – Eski/sorunlu",
                           "C": "C – Yetersiz", "D": "D – İyi", "U": "U – Erişilemedi, doğrulanamadı"}[wstat],
            "web_puani": ws,
            "web_analiz": "; ".join(f"{n}: {p} ({w})" for n, p, w in wbr),
            "gorsel_inceleme": (f"{vis['grade']}/5 – {vis['note']}" if vis else ""),
            "web_teknik": ", ".join((a or {}).get("tech", [])) + (f"; © {a.get('copyright_year')}" if a and a.get("copyright_year") else ""),
            "firma_buyuklugu": next((w for n, p, w in pbr if n == "Kurumsal büyüklük"), ""),
            "kurumsal_ozet": mo.get("summary") or (l.get("desc") or (a or {}).get("meta_desc", ""))[:400],
            "linkedin": social.get("linkedin", "") or mo.get("linkedin", ""),
            "instagram": social.get("instagram", "") or mo.get("instagram", ""),
            "diger_sosyal": ", ".join(v for k, v in social.items() if k not in ("linkedin", "instagram")),
            "yetkili": mo.get("owner", ""),
            "kaynaklar": " | ".join(l["sources"] + ([l["web"]] if l["web"] else [])),
            "potansiyel_puani": ps,
            "potansiyel_detay": "; ".join(f"{n}: {p} ({w})" for n, p, w in pbr),
            "lead_kategorisi": cat,
            "oncelik": {"A+": "1-Çok yüksek", "A": "2-Yüksek", "B": "3-Orta", "C": "4-Düşük"}[cat],
            "standart_kapsam": mo.get("scope", "Standart kurumsal site (40.000 TL + KDV) uygun"),
            "satis_yaklasimi": mo.get("approach", ""),
            "eposta_taslagi": mo.get("draft_ref", ""),
            "gonderim_durumu": mo.get("sent", "Gönderilmedi"),
            "demo_durumu": mo.get("demo", "Yok"),
            "durum": mo.get("status") or ("E-posta bulundu" if email else "Araştırılıyor"),
            "sonraki_islem": mo.get("next", ""),
            "arastirma_tarihi": TODAY,
            "inceleme_tarihi_web": (a or {}).get("checked_at", ""),
            "notlar": mo.get("notes", ""),
        })
    # merge duplicates (same company, second domain) into the primary record
    dups = {k: v["duplicate_of"] for k, v in manual.items() if v.get("duplicate_of")}
    prim = {r["key"]: r for r in rows}
    for k, target in dups.items():
        if k in prim and target in prim:
            prim[target]["notlar"] = (prim[target]["notlar"] + f" Mükerrer kayıt birleştirildi: {prim[k]['web_sitesi'] or prim[k]['firma_adi']} aynı firmaya ait (aynı e-posta/telefon).").strip()
            prim[target]["kaynaklar"] += " | " + prim[k]["kaynaklar"]
    rows = [r for r in rows if r["key"] not in dups]
    for i, r in enumerate(sorted(rows, key=lambda r: -r["potansiyel_puani"])):
        r["lead_id"] = f"DJ-ENV-{i+1:03d}"
    rows.sort(key=lambda r: -r["potansiyel_puani"])
    json.dump(rows, open("data/crm_leads.json", "w"), ensure_ascii=False, indent=1)
    with open("data/crm_leads.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(len(rows), "leads")
    print(Counter(r["lead_kategorisi"] for r in rows))
    print(Counter(r["web_durumu"][:2] for r in rows))
    print(Counter(r["eposta_durumu"] for r in rows))


if __name__ == "__main__":
    main()
