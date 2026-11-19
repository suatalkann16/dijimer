# Dijimer Bilişim – B2B Lead Operasyonu

Kampanya 1: **Çevre teknolojileri / su ve atıksu arıtma** – kurumsal web sitesi (40.000 TL + KDV) satışı.

| Dosya | İçerik |
|---|---|
| `rapor/TUR1_RAPOR.md` | Tur 1 raporu: sayılar, Top 20, demo önerileri, aksiyonlar |
| `Dijimer_CRM_Cevre_Teknolojileri.xlsx` | CRM: tüm leadler, Top 20, **Onay Listesi**, doğrulanacaklar, alt sektör haritası |
| `outreach/eposta_taslaklari.md` | 24 kişiselleştirilmiş e-posta taslağı (**hiçbiri gönderilmedi**) |
| `rapor/kanitlar/` | İlk 30 adayın site ekran görüntüleri |
| `docs/yontem.md` | Kaynaklar, puanlama ve doğrulama kuralları |
| `data/` | `crm_leads.csv/json` (CRM), `audits.json` (teknik denetim), `visual.json` (görsel inceleme), `manual.json` (araştırma notları) |
| `tools/` | Tekrar çalıştırılabilir araç zinciri |

## Güncelleme akışı
```bash
python3 tools/batch_audit.py urls.txt        # yeni siteleri denetle
python3 tools/build_crm.py                    # birleştir + puanla + mükerrer kontrolü
python3 tools/export_xlsx.py                  # Excel'i yeniden üret
```
Gönderim kuralı: yalnızca Onay Listesi'nde **Onaylandı** yazılan e-postalar, tek tek gönderilir.
