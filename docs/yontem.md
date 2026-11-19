# Yöntem – Tur 1 (19.11.2026)

## Kaynaklar
- Web araması: Bursa, İstanbul, Kocaeli, İzmir, Ankara, Balıkesir, Sakarya, Eskişehir ve Tekirdağ için şehir + alt sektör kombinasyonlarıyla 30'dan fazla farklı sorgu (su arıtma, atıksu, paket arıtma, RO, filtre pres, çevre danışmanlık, ölçüm laboratuvarı, atık yönetimi, proses tankı, kazan suyu kimyasalları, havuz ekipmanı, SEÖS).
- Firma rehberi: kurumsal.web.tr "Arıtma" sektörünün tamamı (182 kayıt, ayrıntı sayfalarıyla). E-postalar Cloudflare kodlamasından çözüldü.
- Ek kaynaklar: Çorlu TSO rehberi, Makinaturkiye, Endustri.io, kariyer.net firma profilleri, sektörel haberler (Ekonomi Gazetesi, Bursa Hakimiyet, DHA).
- Firmaların resmi web siteleri: ana sayfa, iletişim, hakkımızda, referans ve proje sayfaları.
- Erişilemeyen rehberler: firmasec.com, aritmafirmarehberi.com (alan adı çözülmüyor).

## Mükerrer kontrolü
Alan adı (yoksa normalize edilmiş firma adı) anahtar olarak kullanıldı. Aynı e-posta veya telefonu paylaşan kayıtlar tek firmada birleştirildi (3 birleştirme yapıldı).

## Web sitesi kategorisi
- **A – Yok:** Resmi site yok, alan adında yalnızca hosting varsayılan sayfası var ya da site "yenileniyor" sayfasında. Birden fazla kaynakla kontrol edildi: rehberde "site yok" görünen MCY, Sistempark, Çevyap, Yeşil Çevre, Ekoçed, Çedfem ve Netçevre'nin aslında sitesi olduğu bulundu ve A'ya alınmadı.
- **B – Eski/sorunlu**, **C – Yetersiz**, **D – İyi:** Teknik denetim ve görsel inceleme birlikte değerlendirildi.
- **U – Erişilemedi, doğrulanamadı:** Bağlantı reddi, SSL hatası, yalnızca HTTP. "Site yok" varsayımı yapılmadı. Bazı Türk hosting firmaları yurt dışı IP'leri engelliyor; bu kayıtlar Türkiye'den tekrar kontrol edilmeli.

## Web sitesi puanı (100)
Tasarım 20 · Mobil 15 · Kullanıcı deneyimi 15 · İçerik 15 · Hizmet sunumu 10 · Referans/proje 10 · SEO/teknik 10 · İletişim/dönüşüm 5.
- Teknik sinyaller `tools/site_audit.py` ile toplandı: HTTPS, viewport, başlık/meta, telif yılı, CMS, görsel sayısı, kelime sayısı, menü yapısı, referans/proje sayfası, İngilizce sürüm, e-posta ve telefon.
- Tasarım puanı 186 sitenin masaüstü ve mobil ekran görüntülerinin **tek tek görsel incelemesiyle** (1–5 not) belirlendi.
- Tarayıcıda "upstream request failed" veya boş ekran görülen siteler, bu çalışma ortamının bağlantısından kaynaklanabileceği için "kırık site" sayılmadı ve "teyit edilmeli" olarak not edildi.

## Potansiyel puanı (100)
Web sitesi ihtiyacı 30 · Kurumsal büyüklük 20 · Ticari potansiyel 20 · Dijital gelişim fırsatı 15 · İletişim bilgileri 15.
- Kurumsal büyüklük: üretim/imalat, anahtar teslim/taahhüt, ihracat, ISO/TÜRKAK, kuruluş yılı ve kamu/OSB projeleri gibi sitede ya da rehberde geçen kanıtlar.
- Elle düzeltmeler (`data/manual.json`): araştırma bulgusu olan firmalara gerekçeli artı ya da eksi puan. Perakende ev tipi cihaz bayileri B ile sınırlandı. A+ için doğrulanmış iletişim şartı arandı.
- Sınıflar: A+ 85–100 · A 70–84 · B 50–69 · C 0–49.

## E-posta doğrulama sınıfları
- **Doğrulanmış – resmi web sitesi:** Firmanın kendi sitesinde yayımlanan, firmanın alan adındaki adres.
- **Doğrulanmış – … (aynı marka, farklı uzantı / farklı kurumsal alan adı / ücretsiz e-posta servisi):** Sitede yayımlanan, firmaya ait olduğu içerikten anlaşılan adres. Ücretsiz servis adresi yalnızca firma adıyla eşleşiyorsa kabul edildi.
- **Güvenilir kaynak:** Firma rehberi kaydı.
- **Tahmini – doğrulanmadı:** Sitede geçen ama firmaya ait olduğu kanıtlanmayan adres (tema/ajans geliştiricisi vb.). **Gönderime hazır değildir.**
- Hiçbir adres tahminle üretilmedi.

## Araçlar
`tools/` klasörü: `site_audit.py` (teknik denetim), `batch_audit.py`, `crawl_kurumsal.py` (rehber taraması), `shots_par.js` (ekran görüntüleri), `contact_sheet.py`, `deep_pages.py` ve `facts.py` (kurumsal araştırma), `score.py` (puanlama), `build_crm.py` (birleştirme, mükerrer kontrolü, CRM), `export_xlsx.py` (Excel).
