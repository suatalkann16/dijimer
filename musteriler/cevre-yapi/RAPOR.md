# Çevre Yapı Arıtma Sistemleri — Dijital Analiz, Web Sitesi Konsepti ve Satış Planı

*Dijimer Bilişim için hazırlanmıştır · Kasım 2026 · Dahili çalışma dokümanı*

---

## Yönetici özeti

- **Firma:** Bursa merkezli, 2006'da Çevre Mühendisi Çağlar Özçelikler'in kurduğu atıksu arıtma mühendislik ve taahhüt firması. Yaklaşık 30 kişilik ekipte 6 çevre ve 2 inşaat mühendisi çalışıyor. Resmi proje listesinde **98 tesis** yer alıyor. Bu tesislerin **toplam tasarım kapasitesi 137.096 m³/gün**. Projeler **24 ilde** ve listede **5 ülkede** (Rusya, ABD, Romanya, Özbekistan, Kazakistan) bulunuyor. Firma 2026'da 20. yılını kutluyor.
- **Dijital durum:** Site 2024 sonunda WordPress/Elementor ile yenilenmiş, ancak içerik firmanın gerçek ölçeğini yansıtmıyor. Proje detay sayfaları boş. Haberler yalnızca gazete küpürü görseli olarak duruyor. Meta açıklamaları yok. Telefon ve e-posta tıklanabilir değil. Teklif formu yok. İngilizce site başlığı "Environmental Building Treatment Systems". Sitede yayında kalmış "Sample Page" ve "lorem ipsum" sayfaları var.
- **Fırsat:** Kamu ve OSB ihalelerinde referans gösterme, yurt dışı hedefi (Kuzey Afrika) ve 20. yıl iletişimi. Bu üç ihtiyaç, güçlü bir proje portföyü sitesini doğrudan iş geliştirme aracına çeviriyor.
- **Hazırlanan çalışma:** Next.js ile geliştirilmiş, çalışan, 154 sayfalık bir konsept site. 98 proje ayrı sayfada ve filtrelenebilir. Proje haritası, teklif formu ve mobil uyum dahil. Tüm içerik firmanın kendi yayımladığı verilere dayanıyor.
- **Önerilen fiyat:** 165.000 – 240.000 TL + KDV ("Önerilen" paket). Ayrıntılar bölüm J'de.

---

## A. Şirket araştırması

### Kimlik
| Konu | Bulgu | Kaynak |
|---|---|---|
| Unvan | Çevre Yapı Arıtma Sistemleri San. ve Tic. Ltd. Şti. | Basın (Kütahya OSB sözleşme haberleri) |
| Kuruluş | 2006, Bursa | cevre-yapi.com/tr/kurumsal/hakkimizda |
| Kurucu | Çağlar Özçelikler, Çevre Mühendisi, Yönetim Kurulu Başkanı, BUÜ Çevre Müh. mezunu | Site, basın |
| Yönetim | Berrin Özçelikler, Orman Mühendisi, YK Başkan Yardımcısı. Kadın Girişimciler sitesinde köşe yazarı, basın ilişkilerinde aktif | Ekibimiz sayfası, haberler |
| Çalışan | "6'sı çevre, 2'si inşaat mühendisi olmak üzere toplam 30 çalışma arkadaşı" | Başkanın Yazısı |
| Adres | Altınşehir Mah. 207. (280) Sok. No:84 Nilüfer/Bursa | İletişim sayfası |
| İletişim | +90 (224) 443 58 95 · info@cevre-yapi.com | İletişim sayfası |
| Üyelikler | BTSO, KalDer, TMMOB Çevre Mühendisleri Odası, TÜMKAD | Üyeliklerimiz |
| Sosyal | LinkedIn, Instagram (@cevre_yapi), Facebook | Site alt bilgisi |

### Ölçek ve faaliyet
- Resmi proje tablosu 2006–2025 arasında **98 tesis** içeriyor: 49 endüstriyel AAT, 25 endüstriyel + evsel AAT, 13 evsel AAT ve çeşitli kapasite artışı, M/E, sızıntı suyu, proses suyu, projelendirme ve işletme işleri.
- Müşteri grupları: **18 OSB**, **11 belediye/kamu** (KOSKİ, MESKİ, Konya BB, Edirne Subaşı Bld.) ve sanayi. Sanayi müşterileri arasında Bosch, Arçelik, Türk Traktör, Anadolu Isuzu, BMC, Karsan, MAN, Tırsan, Nobel İlaç, 3M, Hidromek, BP, Anadolu Cam, Ruscam, Çanakkale Seramik, Asil Çelik ve Carrefour var.
- **Yurt dışı:** Proje listesinde Rusya (2012, 2019), ABD (2016), Kazakistan (2016), Özbekistan (2016, 2017, 2023) ve Romanya (2019, 2024) yer alıyor. Basına göre (Ekohaber, 09.07.2024) Bulgaristan ve Türkmenistan'da da işler yapılmış. Yurt dışındaki 10. tesis Romanya'da tamamlanmış ve **yeni hedef Kuzey Afrika** (Mısır, Cezayir, Fas) olarak açıklanmış.
- **Son dönem işler:**
  - **HAB Ankara Uzay ve Havacılık OSB:** 4.000 m³/gün, 31.05.2023–31.05.2024, 90.000 m² alan, işletme dahil. YK Başkanı bu işi "bugüne kadarki en önemli projemiz" diye tanımlıyor.
  - ASO 2. ve 3. OSB etapları.
  - **2024'te 10 tesis**, günde toplam 15 bin m³ kapasite.
  - Buharkent OSB sözleşmesi (Aralık 2024).
  - **Kütahya OSB AAT Kapasite Artırım Projesi:** Sözleşme Ağustos 2026'da imzalandı. Tesis kapasitesi 15.000 m³/gün'e çıkacak.
- **Kamuoyu iletişimi:** Firma düzenli basın bülteni yayımlıyor (Dünya Su Günü, su ayak izi, müsilaj, Yeşil OSB, karbon riski). Bursa yerel basınında ve Dünya, Ekohaber gibi ekonomi basınında görünür. Bu iletişim web sitesine yansımıyor.
- **Akademi:** BUÜ Çevre Mühendisliği Bölümü'ne "Çevre Yapı Eğitim ve Toplantı Salonu" kazandırılmış. Firma bölümün açılış dersini vermiş ve dereceyle mezun olan öğrencileri ödüllendirmiş.

### Hizmetler (sitedeki 9 faaliyet alanı)
| Hizmet | Ne çözüyor | Kanıt / referans |
|---|---|---|
| Endüstriyel AAT yapımı | Sektöre özgü kirleticiler: fiziksel, kimyasal arıtma, çamur susuzlaştırma, yağ tutucu | 74 endüstriyel veya karma proje |
| Evsel AAT yapımı | Paket (50–1000 kişi) ve betonarme (>1000 kişi) biyolojik arıtma | KOSKİ, MESKİ, Carrefour |
| Endüstriyel AAT işletmesi | Kurulan tesisin standartlara uygun işletilmesi | HAB ve Bilecik OSB'de görevli işletme mühendisleri |
| Evsel AAT işletmesi | Belediye tesislerinin işletmesi | KOSKİ tesisleri (yapım + işletme), Sincan Cezaevi |
| Proses suyu hazırlama | Demineralizasyon, RO, yumuşatma, EDI, ozon, aktif karbon | Asil Çelik, 16.800 m³/gün |
| Online ölçüm | KOİ, BOİ, TSS, TOC, DOC, nitrat/nitrit, CDOM, yağ, renk, siyanobakteri, iletkenlik | — |
| Partiküler/emisyon arıtma | PP/PE gaz yıkayıcılar (scrubber), asit buharı ve koku arıtımı | Kendi imalatları |
| Endüstriyel tank imalatı | PP/PE/PVC kaplama banyoları ve dozlama tankları | Metal kaplama sektörü (ör. İstanbul Cila ve Nikelajcılar Sitesi) |
| Mühendislik hizmetleri | Tasarım, taahhüt, servis-bakım, danışmanlık | Sivas 1. OSB projelendirme, 8.000 m³/gün |

### Kanıta dayalı güçlü yönler
1. **Uçtan uca kapsam:** Projelendirme, inşaat, mekanik/elektrik, otomasyon ve işletme. 11 tesiste işletme de kapsamda.
2. **Kamu/OSB deneyimi:** 29 kamu ve OSB işi. İhale ve şartname disiplini var.
3. **Sektör çeşitliliği:** 9 sektör grubu. Otomotivden ilaca, seramikten enerjiye.
4. **Ölçek aralığı:** 5 m³/gün'lük fabrika tesislerinden 16.000+ m³/gün'lük OSB ve proses suyu tesislerine.
5. **Uluslararası iş bitirme:** 5–7 ülke ve Kuzey Afrika hedefi.
6. **Kurumsal itibar:** Düzenli basın varlığı, akademi iş birlikleri, 20. yıl.

### Notlar ve tutarsızlıklar (müşteriye nazikçe iletilebilir)
- Sitedeki sayaçlar birbirini tutmuyor. Hakkımızda sayfası "99 proje / 126.496 m³", Kurumsal sayfası "96 / 126.988" diyor. "5 ülke" sayacı ile Başkanın Yazısı'ndaki "dokuz ülke" ifadesi de çelişiyor. Proje tablosundan hesaplanan değerler 98 tesis ve 137.096 m³/gün.
- Google Maps puanı, LinkedIn takipçi sayısı ve YouTube içerikleri bu oturumda doğrulanamadı (ağ kısıtı). Sunumdan önce elle kontrol edilmeli.

---

## B. Dijital durum analizi (cevre-yapi.com/tr)

Ekran görüntüleri: `docs/ekran-goruntuleri/mevcut-*.png`

### Tasarım
- **Olumlu:** Kurumsal mavi-yeşil palet tutarlı. Logo ve "20. yıl" vurgusu var. Menü yapısı mantıklı.
- **Zayıf:**
  - Görsel hiyerarşi düz, başlıkların tamamı büyük harf.
  - Otomatik tarayıcı testimizde ilk ekranda hero slider görünmedi; sayfa doğrudan "Neler yapıyoruz" kutularıyla açıldı.
  - Proje fotoğrafları küçük kullanılmış.
  - Tema bileşenleri (Elementor + JetEngine + Slider Revolution) şablon hissi veriyor.
  - Ana sayfa 33 script ve 7 stil dosyası yüklüyor.

### Kullanıcı deneyimi
| Soru | Durum |
|---|---|
| Ziyaretçi firmayı ilk 5 saniyede anlıyor mu? | Kısmen. Net bir değer önerisi başlığı yok. |
| Uzmanlıklar net mi? | Liste var, ancak hizmet sayfaları 1–3 paragraf; referans ve kanıt bağlantısı yok. |
| Projeler etkili sunuluyor mu? | **Hayır.** Liste sayfası tablodan ibaret. **Proje detay sayfaları boş** (yalnızca başlık ve "Proje Detayları" etiketi). Filtre yok, fotoğraflar kullanılmıyor. |
| İletişime geçmek kolay mı? | Telefon ve e-posta **tıklanabilir değil** (`tel:`/`mailto:` yok). Tek form var (ad, e-posta, mesaj). |
| Teklif süreci | **Teklif formu yok.** Debi, sektör ve lokasyon toplanmıyor. |
| CTA'lar | Ana sayfada "İncele" ve "Tüm projeleri görüntüle" dışında dönüşüm odaklı CTA yok. |
| Kariyer | "Aktif ilan yok" mesajı var, genel başvuru imkânı yok. |

### SEO
- Title tüm ana sayfada yalnızca "Çevre Yapı Arıtma Sistemleri". **Meta description yok.**
- Ana sayfada **4 adet H1, 0 adet H2** var. Başlık yapısı bozuk.
- Ana sayfadaki 33 görselin **20'sinde alt metin boş**. Referans logolarının alt metinleri de boş.
- URL'lerde yazım hataları var: `/kurumsal/kalita-politikamiz/`, `/faliyet-alani/`.
- **Haber içerikleri yalnızca gazete küpürü görseli.** Google metni okuyamadığı için indekslenebilir içerik yok. Firmanın düzenli basın faaliyeti SEO'ya dönüşmüyor.
- Proje detay sayfaları boş: 98 potansiyel uzun kuyruk açılış sayfası ("Konya evsel atıksu arıtma tesisi", "OSB atıksu arıtma tesisi yapımı" vb.) kullanılmıyor.
- Yayında kalmış artıklar: `/tr/sample-page/` (WordPress örnek sayfası) ve `/tr/etkinliklerimiz/lorem-ipsum/`.
- Alt bilgide "Copyright © 2014" yazıyor.
- **Uluslararası SEO:** İngilizce sürüm var (TranslatePress), ancak site başlığı "Environmental Building Treatment Systems" olarak çevrilmiş. Firma adı marka olarak korunmalı. Kuzey Afrika hedefi için Fransızca/Arapça içerik yok.
- **Yapısal veri** (Organization, LocalBusiness) yok. Yerel SEO için Google İşletme Profili ile tutarlılık kontrol edilmeli.

### Dönüşüm envanteri
| Unsur | Mevcut | Öneri |
|---|---|---|
| Proje detay sayfaları | Boş | Künye, proses, kapasite, fotoğraf |
| Teklif talep formu | Yok | Debi, sektör, aşama ve lokasyon alanlı form |
| Teknik danışmanlık talebi | Yok | Teklif formuna "aşama" seçeneği olarak eklendi |
| Tıklanabilir telefon/e-posta | Yok | Eklendi |
| WhatsApp | Yok | Firma bir WhatsApp Business hattı onaylarsa eklenebilir |
| İndirilebilir firma sunumu (PDF) | Yok | Faz 2: TR/EN kurumsal sunum ve referans listesi |
| Referanslar | Logo ızgarası (alt metinsiz) | Sektöre göre gruplu ve projeye bağlanan liste |

---

## C. Fırsatlar

1. **Proje portföyünü satış aracına çevirmek.** 98 proje sayfası; OSB ve belediye ihale komisyonları ile sanayi satın almacıları için "benzer iş bitirme" kanıtı.
2. **Kuzey Afrika ve yurt dışı:** EN + FR (+ AR) sürüm; "International projects" bölümü.
3. **20. yıl kampanyası:** Kilometre taşları, yıl dönümü içerikleri, basın bültenlerinin metin olarak yayımlanması.
4. **Basın faaliyetini SEO'ya bağlamak:** Her bülten indekslenebilir bir makale olmalı (şu an yalnızca görsel).
5. **Teklif hunisi:** Yapılandırılmış teklif formu, CRM/e-posta bildirimi ve ileride sektörel açılış sayfaları.
6. **Saha görseli:** Drone ile kısa bir çekim programı (Kütahya OSB, HAB, KOSKİ). Mevcut fotoğraflar kaliteli ama sayıca az: 98 projeden yalnızca 8'inin fotoğrafı var.
7. **LinkedIn:** Proje sayfalarının LinkedIn'de paylaşılması (B2B karar vericiler orada).

---

## D. Rakip ve benchmark analizi

> **Not:** Bu oturumda ağ politikası nedeniyle rakip sitelere doğrudan erişilemedi. Değerlendirme, kamuya açık bilgilere ve bu firmaların bilinen site yaklaşımlarına dayanıyor. Sunumdan önce Dijimer ekibinin siteleri bir kez gezmesi önerilir.

| # | Firma | Tür | İlham alınan unsur | Çevre Yapı'ya uyarlama |
|---|---|---|---|---|
| 1 | **Artaş** (artas.com.tr) | TR, 1982'den beri çevre teknolojileri | Referansları nüfus eşdeğeri ve kapasiteyle sunma; anahtar teslim + işletme vurgusu | Her projede debi ve proses künyesi |
| 2 | **ENTA Arıtma** | TR, endüstriyel arıtma, 20+ OSB referansı | Rakamlarla güven (tesis sayısı, OSB sayısı, ülke sayısı) | Rakamlar tablodan hesaplanıyor, doğrulanabilir |
| 3 | **Çevtaş Çevre Teknolojisi** | TR, ulusal/uluslararası anahtar teslim taahhüt | Taahhüt odaklı kurumsal anlatım | "Uçtan uca sorumluluk" bloğu |
| 4 | **Artemis Arıtım** | TR, çok dilli içerik | Çok dilli (TR/EN/FR/DE) içerik ve blog | Faz 2: EN/FR ve indekslenebilir haber |
| 5 | **Veolia Water Technologies** | Global | Sektör (endüstri) bazlı navigasyon, vaka çalışmaları | Sektör sayfaları ve proje "notları" |
| 6 | **VA Tech WABAG** | Global, belediye + endüstri EPC | Filtrelenebilir referans listesi, kapasite verisi | Filtreli proje gezgini + tablo görünümü |
| 7 | **Metito** | Global, MENA odaklı | Bölge/ülke bazlı proje haritası | Türkiye haritası ve yurt dışı listesi |
| 8 | **Aquatech** | Global, endüstriyel su | Proses ve teknoloji anlatımı, "çözüm" dili | Proses zinciri bölümü (4 kademe ve kullanım sayıları) |
| 9 | **Xylem** | Global | Net CTA'lar, "uzmana danışın" formları | Her sayfada sabit teklif CTA'sı |
| 10 | **Biwater** | Global EPC + işletme | İşletme ve bakım hizmetinin ayrı ürün gibi sunulması | "İşletme & Mühendislik" hizmet grubu |

**Sonuç:** Türk rakiplerin çoğu Çevre Yapı'ya benzer, şablon tabanlı WordPress siteleri kullanıyor. Uluslararası firmaların farkı üç noktada: **veri odaklı proje portföyü**, **sektör bazlı anlatım** ve **güçlü dönüşüm noktaları**. Konsept bu üçünü Çevre Yapı ölçeğine uyarlıyor. Hiçbir siteden tasarım veya içerik kopyalanmadı.

---

## E. Yeni site stratejisi

**Konumlandırma cümlesi:** *"Atıksuyu mühendislikle temiz suya dönüştürüyoruz."* Yanında üç kanıt veriliyor: 98 tesis, 137.096 m³/gün, 24 il ve 5 ülke.

**Tasarım kararları**
- **Renk:** Logodaki #005CAA (mavi) ve #0BA13B (yeşil) korundu. Derin lacivert (#04182D) zemin, mühendislik ağırlığı ve premium his için eklendi. Yeşil yalnızca vurgu ve CTA'da kullanılıyor.
- **Logo:** Değiştirilmedi. Koyu zeminler için yalnızca mavi öğeleri beyaza çevrilmiş bir "reverse" varyant üretildi. Müşteriye ayrıca belirtilmeli.
- **Tipografi:** Archivo (geniş, endüstriyel karakterli başlık fontu) ve Inter (okunaklı gövde). Türkçe karakter desteği tam, fontlar yerelde barındırılıyor.
- **İmza motif:** Logodaki kare ve çizgilerden türetilen teknik çizim dili: köşe işaretleri, blueprint ızgara, numaralı bölümler, proses akış okları.
- **Görsel dürüstlük:** Yalnızca firmanın kendi fotoğrafları kullanıldı. Fotoğrafı olmayan projelerde stok görsel yerine **teknik veri kartı** (debi, proses, tür) gösteriliyor. Böylece hiçbir temsili görsel gerçek proje gibi sunulmuyor.
- **Bilgi mimarisi:** Proje, sektör ve hizmet sayfaları birbirine çapraz bağlı. Her hizmet kendi referans projelerini, her proje kendi sektörünü gösteriyor.
- **Dönüşüm:** Her sayfada "Teklif Talebi". Yapılandırılmış teklif formu var. Telefon ve e-posta tıklanabilir.

---

## F. Geliştirilen web sitesi

**Konum:** `/home/user/cevre-yapi-konsept`

**Teknoloji:** Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS 4. Ağır kütüphane kullanılmadı: harita bir SVG olarak derleme anında üretiliyor, animasyonlar yalnızca CSS ve IntersectionObserver ile yapılıyor. Ortak JS yükü yaklaşık 103 kB, ana sayfa ilk yüklemesi yaklaşık 136 kB.

**Sayfalar (154 statik sayfa + 1 API)**
| Sayfa | İçerik |
|---|---|
| Ana sayfa | Gerçek proje fotoğraflı hero slider, rakamlar, kurumsal giriş + başkan alıntısı, 3 hizmet grubu, proses zinciri (kademe başına tesis sayısı), öne çıkan HAB vakası + 4 proje, etkileşimli Türkiye haritası, 9 sektör, "Neden Çevre Yapı", referans şeridi, haberler, CTA |
| Kurumsal | Hikâye, 2006–2026 kilometre taşları, misyon/vizyon, değerler, yönetim ve ekip, başkan alıntısı, kalite politikası, üyelikler |
| Hizmetler + 9 detay | Yaşam döngüsü, gruplu hizmetler; her detayda metin, tipik proses akışı, özellikler, referans projeler, sabit CTA |
| Projeler + 98 detay | Arama, sektör/tür/şehir-ülke/yıl filtreleri, URL senkronizasyonu, kart ve tablo görünümü, 4 sıralama, "daha fazla göster", harita. Detayda künye, proses zinciri, iş kapsamı, kapasite, galeri, basın notları (HAB), benzer projeler, önceki/sonraki gezinme |
| Sektörler + 9 detay | Sektör ihtiyacı, yaklaşım, öne çıkan tesisler, tüm proje tablosu |
| Referanslar | 98 kurum, sektöre göre gruplu ve projelere bağlı |
| Sürdürülebilirlik | Etki rakamı, 4 ilke, akademi iş birliği, görüş yazıları |
| Haberler + 19 detay | Metin özetleri ve basın küpürü galerileri |
| Kariyer | Neden Çevre Yapı, açık pozisyon durumu, genel başvuru formu |
| İletişim | Tıklanabilir telefon/e-posta, adres, yol tarifi, form, Google Harita |
| Teklif Talebi | İki adımlı form (proje bilgileri + iletişim) ve "sonraki adımlar" paneli |
| KVKK, Çerez, 404 | Taslak yasal metinler (hukuk onayı gerekli), markalı 404 |

**Teknik ve SEO özellikleri**
- Sayfa bazında title, description ve canonical. Open Graph görseli. Organization, BreadcrumbList, NewsArticle ve CreativeWork JSON-LD. Otomatik `sitemap.xml` ve `robots.txt`.
- **Konsept modu:** Üstte "Tasarım konsepti — resmi web sitesi değildir" bandı, `noindex` meta etiketi ve `X-Robots-Tag` başlığı. Canlıya alırken tek değişkenle kapatılıyor.
- **İsteğe bağlı parola koruması** (`DEMO_USER` / `DEMO_PASS`).
- **Formlar:** Sunucu tarafı doğrulama, honeypot, IP hız sınırı, KVKK onayı. `FORM_WEBHOOK_URL` ile e-posta veya CRM'e bağlanabiliyor.
- **Erişilebilirlik:** "İçeriğe geç" bağlantısı, odak halkaları, `aria-expanded` menüler, Escape ile kapanma, form hata mesajlarının alanlara bağlanması, `prefers-reduced-motion` desteği, harita için klavye erişimi ve metin alternatifi.
- **Güvenlik başlıkları:** nosniff, Referrer-Policy, X-Frame-Options, Permissions-Policy.
- **Dijimer markası sitede yok.**

**Test sonuçları**
- Üretim derlemesi hatasız (TypeScript + lint).
- 22 rota HTTP kontrolünden geçti (404 dahil).
- 1440 px masaüstü ve iPhone 13 görünümlerinde tam sayfa ekran görüntüsü alındı. Yatay taşma ve konsol hatası yok.
- 20/20 etkileşim testi geçti: mega menü, mobil menü, filtreler ve URL senkronu, arama, tablo görünümü, harita derin bağlantısı, "daha fazla", iletişim ve teklif formlarında hata ve başarı akışları, hata sonrası değerlerin korunması, 177 iç bağlantının tamamı 200.
- Parola koruması doğrulandı: kimlik bilgisi olmadan 401, doğru bilgiyle 200.

**Bilinçli sınırlar (konsept kapsamı)**
- İçerik yönetim paneli yok; veriler kod içindeki dosyalarda duruyor. Gerçek projede headless CMS (Payload/Strapi/Sanity) veya mevcut WordPress'in headless kullanımı önerilir.
- Yalnızca Türkçe.
- Team fotoğrafları yerine baş harfler kullanıldı (tutarsız fotoğraf seti ve kişisel veri hassasiyeti nedeniyle).
- KVKK ve çerez metinleri taslaktır.

---

## G. Demo

**Yerelde çalıştırma**
```bash
cd /home/user/cevre-yapi-konsept && npm install && npm run build && npm start
```
Ardından http://localhost:3000 adresini açın.

**Müşteriye gönderilecek bağlantı:** Bu oturumdan herkese açık bir önizleme bağlantısı **oluşturulmadı**. Site gerçek bir firmanın adını, logosunu ve iletişim bilgilerini taşıdığı için yayının Dijimer'in kendi hesabından, kontrollü yapılması gerekiyor.

Önerilen yol (yaklaşık 10 dakika):
1. Projeyi Dijimer'in GitHub hesabına yükleyin. Vercel'de "Import Project" ile içe aktarın.
2. Ortam değişkenlerini girin: `DEMO_USER`, `DEMO_PASS` ve `NEXT_PUBLIC_SITE_URL`. Konsept modu varsayılan olarak açık (bant + noindex).
3. Alan adı olarak örneğin `cevreyapi-konsept.vercel.app` veya `konsept.dijimerbilisim.com` kullanın. **cevre-yapi.com'a veya firmanın hostingine dokunmayın.**

---

## H. E-posta

- **Alıcı:** info@cevre-yapi.com (resmi sitede yayımlanan genel adres)
- **Taslak:** `docs/EPOSTA-TASLAGI.md`
- **Durum:** Gönderilmedi, onayınızı bekliyor.

---

## I. Satış planı

**1. Gönderim ve takip**
- E-postayı Salı–Perşembe sabah gönderin.
- Aynı gün LinkedIn'de Berrin Özçelikler'e kısa bir bağlantı notu iletin. Basın ve iletişim tarafında en görünür yönetici o; olası ilk karar verici.
- 5 iş günü sonra tek hatırlatma gönderin: *"Geçen hafta paylaştığımız konsepti inceleme fırsatınız oldu mu? Bursa'dayız; isterseniz ofisinizde 20 dakikada gösterebiliriz."*
- 10 iş günü sonra yanıt yoksa telefonla arayın.

**2. Toplantı (Nilüfer, yüz yüze)**
- Demoyu canlı gösterin: HAB proje sayfası, filtre ve harita, teklif formu.
- Mevcut siteyle 3 karşılaştırma yapın: boş proje sayfası, görsel haberler, EN başlık.
- Keşif soruları:
  - Kim güncelliyor?
  - İhalelerde site referans olarak kullanılıyor mu?
  - Kuzey Afrika için hangi diller gerekli?
  - Elde ne kadar fotoğraf ve video var?
  - Teklif talepleri şu an nasıl geliyor?

**3. Beklenen itirazlar**
- *"Sitemiz 2024'te yenilendi."* Mevcut içeriği çöpe atmıyoruz; aynı içeriği satış ve ihale aracına çeviriyoruz. Yapılacak iş bir taşıma, yeniden başlangıç değil. Eski URL'ler 301 yönlendirmeyle korunur.
- *"Pahalı."* Tek bir OSB veya sanayi tesisi işinin bedelinin yanında web yatırımı küçük kalır. Taksitli ve fazlı plan sunulabilir.
- *"Ajansımız var."* (Basın bültenleri bir PR ajansından geliyor olabilir.) Rol ayrımı: PR içerik üretir, biz bu içeriğin yayınlandığı ve indekslendiği altyapıyı kurarız.

**4. Teklif**
- 3 paketli, çapalı fiyat (bölüm J).
- 6–8 hafta takvim:
  - 1. hafta: keşif ve içerik planı
  - 2–3. hafta: tasarım onayı
  - 4–6. hafta: geliştirme ve CMS
  - 7. hafta: EN çeviri ve test
  - 8. hafta: yayın, 301 yönlendirmeler, eğitim
- Ödeme: %40 peşin, %30 tasarım onayında, %30 teslimde. (Dijimer'in mevcut "peşinat + teslim" modeline uyumlu.)

**5. Ek satış (upsell) ve tekrarlayan gelir**
- Bakım/destek aboneliği
- Aylık SEO ve içerik (bültenlerin makaleye çevrilmesi)
- Drone çekimi koordinasyonu
- TR/EN PDF kurumsal sunum
- LinkedIn içerik paketi
- Google İşletme Profili optimizasyonu (Dijimer'in mevcut hizmeti)

---

## J. Tahmini proje fiyatı

**Piyasa referansı (2026, Türkiye, ajans yayınları):**
- Kurumsal site teklifleri geniş bir aralıkta: 15.000 – 200.000 TL.
- Hazır tema: 8.000 – 25.000 TL.
- Özgün tasarım: 40.000 TL'den başlıyor.
- 5–15 sayfalık kurumsal site (İstanbul ajansı): 40.000 – 120.000 TL.
- KOBİ'lerin çoğu 30.000 – 80.000 TL bandında harcıyor.
- Çok dilli yapı, özel entegrasyonlar ve bakım fiyatı belirgin şekilde artırıyor.

(Kaynaklar: braverytechnology.com/tr/web-sitesi-fiyatlari, adaptedijital.com kurumsal web tasarım fiyat yazıları. Ajans blogları olduğu için yön gösterici kabul edilmeli.)

**Bu proje neden "standart kurumsal site" değil**
- 150+ sayfalık veri odaklı yapı (98 proje, 9 hizmet, 9 sektör)
- Filtreli portföy, harita, çok adımlı teklif formu
- Özgün tasarım dili
- İçerik yeniden yazımı
- WordPress'ten taşıma ve 301 haritası
- CMS kurulumu ve çok dilli altyapı

| Paket | Kapsam | Fiyat (KDV hariç) |
|---|---|---|
| **Temel** | Konseptin TR olarak canlıya alınması, basit içerik paneli, 301 yönlendirmeler, form → e-posta, temel SEO | **110.000 – 145.000 TL** |
| **Önerilen** | Temel + **İngilizce** sürüm, headless CMS (projeler, haberler, hizmetler panelden yönetilir), 19 bültenin metne dönüştürülmesi, Google Analytics/Search Console, KVKK çerez onayı, 3 ay destek | **165.000 – 240.000 TL** |
| **Kapsamlı** | Önerilen + **Fransızca** (Kuzey Afrika), TR/EN PDF kurumsal sunum, drone/fotoğraf çekimi koordinasyonu (çekim bedeli hariç), sektörel açılış sayfaları, 12 ay bakım | **280.000 – 380.000 TL** |

**Tekrarlayan hizmetler**
- Bakım ve destek: 4.000 – 7.500 TL/ay
- SEO ve içerik: 12.000 – 20.000 TL/ay
- Barındırma ve alan adı müşteriye ait (Vercel Pro veya VPS: yaklaşık 1.000 – 2.500 TL/ay)

**Öneri:** "Önerilen" paketle açılış yapın (çapa ~210.000 TL). 20. yıl kampanyası kapsamında, ilk toplantıda karar verilirse "İngilizce sürüm dahil" teşviki sunun. Kapsamlı paketi masada tutmak, Önerilen paketin makul görünmesini sağlar.

---

## Ekler

- `docs/ekran-goruntuleri/` — mevcut site ve yeni konseptin masaüstü/mobil görüntüleri
- `docs/EPOSTA-TASLAGI.md` — gönderime hazır e-posta
- `README.md` — teknik kurulum ve yayın
- **Kaynaklar:**
  - cevre-yapi.com (tüm sayfalar ve WordPress REST API; proje tablosu, ekip, haberler, medya)
  - Firmanın "Basında Biz" küpürleri (Ekohaber 09.07.2024, Kütahya Gazetesi 27.08.2026, Yeni Dönem 07.02.2025)
  - Ekonomi Gazetesi ve Gazete Birlik (Kütahya OSB sözleşmesi)
  - Bursa Hakimiyet (genç mühendislere destek, 11.07.2026)
  - Sanayi Gazetesi (ENTA)
  - Kariyer.net (Artaş)
  - dijimerbilisim.com
