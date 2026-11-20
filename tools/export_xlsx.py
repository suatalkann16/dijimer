#!/usr/bin/env python3
"""Export CRM to Excel: data/crm_leads.json + outreach/eposta_taslaklari.md -> Dijimer_CRM_Cevre_Teknolojileri.xlsx"""
import json, re, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

rows = json.load(open("data/crm_leads.json"))
md = open("outreach/eposta_taslaklari.md").read()
subjects = {}
for m in re.finditer(r'<a id="([\w-]+)"></a>\n## (\d+)\. (.+?)\n(.*?)\*\*Konu:\*\* (.+?)\n', md, re.S):
    subjects[m.group(1)] = (int(m.group(2)), m.group(5).strip())

STATUSES = ["Yeni bulundu", "Araştırılıyor", "Araştırma tamamlandı", "E-posta bulundu", "E-posta doğrulandı", "Teklif taslağı hazır",
            "Onay bekliyor", "Gönderildi", "Yanıt bekleniyor", "Olumlu dönüş", "Olumsuz dönüş", "Görüşme planlandı", "Teklif verildi",
            "Satış tamamlandı", "Takip edilecek", "İletişim istemiyor"]
HEAD = PatternFill("solid", fgColor="1F4E78")
CATFILL = {"A+": "C6EFCE", "A": "E2EFDA", "B": "FFF2CC", "C": "F2F2F2"}
wb = Workbook()


def sheet(title, cols, data, widths=None):
    ws = wb.create_sheet(title)
    ws.append([c[1] for c in cols])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for r in data:
        ws.append([r.get(c[0], "") if not callable(c[0]) else c[0](r) for c in cols])
    for i, c in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(c[1], 18)
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    return ws


# --- Özet
ws = wb.active; ws.title = "Özet"
C = collections.Counter
web = C(r["web_durumu"].split(" – ")[0] for r in rows)
cat = C(r["lead_kategorisi"] for r in rows)
ver = sum(1 for r in rows if r["eposta_durumu"].startswith("Doğrulanmış"))
lines = [
    ["Dijimer Bilişim – Çevre Teknolojileri B2B Lead Araştırması (Tur 1)"],
    ["Araştırma tarihi", "2026-11-19"],
    ["Toplam tekil firma", len(rows)],
    ["Web sitesi yok (A, doğrulanmış)", web.get("A", 0)],
    ["Web sitesi bulunamadı – doğrulanacak (A?)", web.get("A?", 0)],
    ["Eski / sorunlu site (B)", web.get("B", 0)],
    ["Yetersiz site (C)", web.get("C", 0)],
    ["İyi site (D)", web.get("D", 0)],
    ["Erişilemedi – doğrulanamadı (U)", web.get("U", 0)],
    ["A+ lead", cat.get("A+", 0)], ["A lead", cat.get("A", 0)], ["B lead", cat.get("B", 0)], ["C lead", cat.get("C", 0)],
    ["Doğrulanmış e-posta (firma sitesi)", ver],
    ["Onaya hazır e-posta taslağı", sum(1 for r in rows if r["eposta_taslagi"])],
    ["Gönderilen e-posta", 0],
    [],
    ["Not", "Hiçbir e-posta gönderilmedi. Tahmini e-postalar gönderime hazır DEĞİLDİR. Puanlama yöntemi: Yöntem sayfası."],
]
for l in lines:
    ws.append(l)
ws["A1"].font = Font(bold=True, size=14)
ws.column_dimensions["A"].width = 48; ws.column_dimensions["B"].width = 90

# --- All leads
allcols = [(k, k) for k in rows[0].keys() if k != "key"]
w = {k: 18 for _, k in allcols}
w.update({"firma_adi": 34, "web_analiz": 60, "potansiyel_detay": 60, "kurumsal_ozet": 60, "satis_yaklasimi": 50, "notlar": 40,
          "kaynaklar": 40, "gorsel_inceleme": 40, "eposta_durumu": 26})
ws = sheet("CRM – Tüm Leadler", allcols, rows, w)
hdr = [c.value for c in ws[1]]
ci = hdr.index("lead_kategorisi") + 1
for row in ws.iter_rows(min_row=2):
    f = CATFILL.get(row[ci - 1].value)
    if f:
        for c in row[:3]:
            c.fill = PatternFill("solid", fgColor=f)
dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=True)
ws.add_data_validation(dv)
col = get_column_letter(hdr.index("durum") + 1)
dv.add(f"{col}2:{col}{len(rows)+1}")
dv2 = DataValidation(type="list", formula1='"Gönderilmedi,Onay bekliyor,Gönderildi,Yanıt bekleniyor,İletişim istemiyor"', allow_blank=True)
ws.add_data_validation(dv2)
col = get_column_letter(hdr.index("gonderim_durumu") + 1)
dv2.add(f"{col}2:{col}{len(rows)+1}")

# --- Top 20
top = [r for r in rows if r["lead_kategorisi"] in ("A+", "A")][:20]
tcols = [("lead_id", "Lead ID"), ("firma_adi", "Firma"), ("sehir", "Şehir"), ("ilce", "İlçe"), ("web_sitesi", "Web sitesi"),
         ("web_durumu", "Web durumu"), ("web_puani", "Web puanı"), ("potansiyel_puani", "Potansiyel"), ("lead_kategorisi", "Kategori"),
         ("eposta", "E-posta"), ("eposta_durumu", "E-posta doğrulama"), ("telefon", "Telefon"), ("alt_sektor", "Alt sektör"),
         ("kurumsal_ozet", "Firma özeti"), ("gorsel_inceleme", "Görsel inceleme"), ("satis_yaklasimi", "Önerilen yaklaşım"),
         ("standart_kapsam", "40.000 TL kapsam değerlendirmesi"), ("sonraki_islem", "Sonraki işlem"), ("notlar", "Notlar")]
sheet("Top 20", tcols, top, {"Firma": 30, "Firma özeti": 70, "Önerilen yaklaşım": 55, "Görsel inceleme": 45, "Notlar": 45,
                            "40.000 TL kapsam değerlendirmesi": 40, "E-posta doğrulama": 28, "Alt sektör": 30})

# --- Approval list
appr = []
for r in rows:
    ref = r["eposta_taslagi"]
    if not ref:
        continue
    anchor = ref.split("#")[-1].strip()
    no, subj = subjects.get(anchor, (int(anchor) if anchor.isdigit() else "", ""))
    appr.append({"no": no, "lead_id": r["lead_id"], "firma_adi": r["firma_adi"], "sehir": r["sehir"], "eposta": r["eposta"],
                 "eposta_durumu": r["eposta_durumu"], "konu": subj, "taslak": ref,
                 "demo": r["demo_durumu"], "onay": "", "onay_tarihi": "", "gonderim": "Gönderilmedi"})
appr.sort(key=lambda x: x["no"] or 99)
acols = [("no", "No"), ("lead_id", "Lead ID"), ("firma_adi", "Firma"), ("sehir", "Şehir"), ("eposta", "Alıcı"),
         ("eposta_durumu", "Doğrulama"), ("konu", "Konu"), ("taslak", "Taslak"), ("demo", "Demo"), ("onay", "ONAY (siz doldurun)"),
         ("onay_tarihi", "Onay tarihi"), ("gonderim", "Gönderim durumu")]
ws = sheet("Onay Listesi", acols, appr, {"Firma": 32, "Alıcı": 30, "Konu": 60, "Taslak": 34, "Doğrulama": 30, "ONAY (siz doldurun)": 20})
dv3 = DataValidation(type="list", formula1='"Onaylandı,Düzenle,Reddedildi,Beklet"', allow_blank=True)
ws.add_data_validation(dv3); dv3.add(f"J2:J{len(appr)+1}")
for c in ws["J"][1:]:
    c.fill = PatternFill("solid", fgColor="FFF2CC")

# --- To verify
ver_rows = [r for r in rows if (r["web_durumu"].startswith("U") or r["eposta_durumu"] == "Bulunamadı") and r["lead_kategorisi"] in ("A+", "A", "B")]
vcols = [("lead_id", "Lead ID"), ("firma_adi", "Firma"), ("sehir", "Şehir"), ("web_sitesi", "Web sitesi"), ("web_durumu", "Web durumu"),
         ("web_analiz", "Neden"), ("eposta_durumu", "E-posta"), ("telefon", "Telefon"), ("kaynaklar", "Kaynak"), ("sonraki_islem", "Sonraki işlem")]
sheet("Doğrulanacaklar", vcols, ver_rows, {"Firma": 32, "Neden": 60, "Kaynak": 50})

# --- Subsector map
subs = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    subs[r["alt_sektor"] or "Belirsiz"][r["lead_kategorisi"]] += 1
ws = wb.create_sheet("Alt Sektör Haritası")
ws.append(["Alt sektör", "Toplam", "A+", "A", "B", "C"])
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = HEAD
for k, v in sorted(subs.items(), key=lambda kv: -sum(kv[1].values())):
    ws.append([k, sum(v.values()), v["A+"], v["A"], v["B"], v["C"]])
ws.column_dimensions["A"].width = 60

# --- Method
ws = wb.create_sheet("Yöntem")
for l in open("docs/yontem.md").read().splitlines():
    ws.append([l])
ws.column_dimensions["A"].width = 160

wb.save("Dijimer_CRM_Cevre_Teknolojileri.xlsx")
print("saved", len(rows), "leads,", len(appr), "drafts,", len(ver_rows), "to verify")
