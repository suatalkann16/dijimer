#!/usr/bin/env python3
"""Print compact research facts from data/pages/<dom>.txt"""
import re, sys
for dom in sys.argv[1:]:
    try: t = open(f"data/pages/{dom}.txt").read()
    except Exception: print("##", dom, "NO PAGES"); continue
    low = t.lower()
    def ctx(pat, n=1, w=110):
        out = []
        for m in re.finditer(pat, t, re.I):
            s = t[max(0, m.start()-w):m.end()+w].replace("\n", " ")
            out.append(s)
            if len(out) >= n: break
        return out
    print("##", dom)
    for lbl, pat, n in [("KURULUŞ", r"(19[5-9]\d|20[0-2]\d)\s*(yılında|yılından|'?[dt]e?n beri|’den beri|senesinde|tarihinde)", 2),
                        ("KURULUŞ2", r"kurul(du|muş|an)", 1),
                        ("İHRACAT", r"ihracat|yurt ?dışı|export|ülke", 2),
                        ("ÇALIŞAN", r"(\d{2,4})\s*(çalışan|personel|kişilik ekip|mühendis)", 1),
                        ("ALAN", r"(\d[\d.]*)\s*m(²|2)\s*(kapalı|açık|alan|tesis|üretim)", 1),
                        ("REFERANS", r"referans", 1),
                        ("ISO", r"iso ?9001|iso ?14001|türkak|yeterlik belgesi|17025", 1),
                        ("ADRES", r"(mah\.|mahallesi|osb|organize sanayi)[^|]{0,90}", 2),
                        ("TEL", r"(\+90|0)\s?\(?\d{3}\)?\s?\d{3}\s?\d{2}\s?\d{2}", 2),
                        ("YÖNETİCİ", r"(genel müdür|kurucu|yönetim kurulu başkanı|şirket sahibi|ceo)", 2)]:
        for c in ctx(pat, n):
            print(f"  [{lbl}] …{c}…")
    m = re.search(r"=== (\S*(hakk|kurumsal|about)\S*)\n(.{0,700})", t, re.I)
    if m: print("  [HAKKINDA]", m.group(3)[:700])
    print()
