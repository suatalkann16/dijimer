#!/usr/bin/env python3
"""Dijimer lead scoring.

Website quality score (0-100, high = good site) and lead potential score
(0-100, high = better sales opportunity), following the campaign brief:

Website (100): design 20, mobile 15, UX 15, content 15, services 10,
               references/projects 10, SEO/technical 10, contact/conversion 5
Potential (100): web need 30, corporate size 20, commercial potential 20,
                 digital opportunity 15, contact info 15

Automatic scores are derived only from signals actually observed on the
site (see tools/site_audit.py). Every sub-score carries a reason string.
Manual overrides from data/manual.json are applied on top and noted.
"""
import re

CUR_YEAR = 2026


def _has(words, *keys):
    return any(k in w for w in words for k in keys)


VIS_DESIGN = {1: 3, 2: 7, 3: 12, 4: 16, 5: 19}
VIS_UX = {1: -5, 2: -3, 3: 0, 4: 2, 5: 3}


def website_score(a, vis=None):
    """a = audit dict, vis = manual visual review {grade 1-5, note}.
    Returns (score or None, breakdown list, status code A/B/C/D/U)."""
    if a is None:
        return None, [("-", 0, "Web sitesi bulunamadı")], "A"
    if not a.get("reachable"):
        if a.get("ssl_error"):
            why = "SSL sertifikası alan adıyla uyuşmuyor; tarayıcı güvenlik uyarısı veriyor"
        elif "ProxyError" in (a.get("error") or ""):
            why = "HTTPS (443) yanıt vermiyor; site yalnızca HTTP olabilir veya kapalı"
        elif a.get("status"):
            why = f"HTTP {a.get('status')} hatası"
        else:
            why = "Bağlantı reddedildi/zaman aşımı"
        return None, [("erişim", 0, "Siteye erişilemedi, doğrulanamadı: " + why)], "U"
    nav = [n.lower() for n in a.get("nav", [])]
    hrefs = [h.lower() for h in a.get("hrefs", [])]
    blob = " ".join(nav + hrefs) + " " + (a.get("home_text", "").lower())
    tech = a.get("tech", [])
    yr = a.get("copyright_year")
    words = a.get("text_words", 0)
    br = []

    # 1. Design & modernity (20)
    d = 10
    why = []
    if yr and yr >= CUR_YEAR - 1:
        d += 4; why.append(f"telif yılı güncel ({yr})")
    elif yr and yr <= CUR_YEAR - 5:
        d -= 5; why.append(f"telif yılı eski ({yr})")
    elif not yr:
        d -= 1; why.append("telif yılı yok")
    if not a.get("viewport"):
        d -= 5; why.append("viewport yok (eski şablon)")
    if any(t in tech for t in ("Elementor", "Tailwind", "Next.js", "React")):
        d += 3; why.append("modern çerçeve/sayfa oluşturucu")
    if "Wix" in tech:
        d -= 2; why.append("Wix hazır şablon")
    if a.get("img_count", 0) < 5:
        d -= 3; why.append("çok az görsel")
    elif a.get("img_count", 0) >= 15:
        d += 2; why.append("zengin görsel kullanımı")
    if "frameset" in tech or "Flash?" in tech:
        d -= 6; why.append("frameset/Flash")
    d = max(0, min(20, d))
    if vis:
        d = VIS_DESIGN[vis["grade"]]
        why = [f"görsel inceleme {vis['grade']}/5: {vis['note']}"] + why
    br.append(("Tasarım ve modernlik", d, ", ".join(why) or "ortalama"))

    # 2. Mobile (15)
    m = 14 if a.get("viewport") else 3
    br.append(("Mobil uyumluluk", m, "viewport meta mevcut (responsive işaret)" if a.get("viewport") else "viewport meta yok; mobilde küçülmüş masaüstü görünümü"))

    # 3. UX (15)
    u = 8
    why = []
    ls = a.get("load_s") or 9
    if ls < 2:
        u += 3; why.append(f"hızlı yanıt ({ls}s)")
    elif ls > 5:
        u -= 3; why.append(f"yavaş yanıt ({ls}s)")
    if a.get("contact_page"):
        u += 2; why.append("iletişim sayfası var")
    else:
        u -= 2; why.append("iletişim sayfası bulunamadı")
    lc = a.get("link_count", 0)
    if lc < 10:
        u -= 3; why.append("çok sınırlı menü/bağlantı")
    elif lc > 40:
        u += 2; why.append("kapsamlı site yapısı")
    if vis:
        u += VIS_UX[vis["grade"]]
    u = max(0, min(15, u))
    br.append(("Kullanıcı deneyimi", u, ", ".join(why)))

    # 4. Content (15)
    if words > 1200:
        c, w = 14, "ana sayfa içeriği zengin"
    elif words > 600:
        c, w = 11, "ana sayfa içeriği yeterli"
    elif words > 250:
        c, w = 7, "ana sayfa içeriği sınırlı"
    else:
        c, w = 3, "ana sayfada çok az metin"
    br.append(("İçerik kalitesi", c, f"{w} (~{words} kelime)"))

    # 5. Services (10)
    if _has(nav + hrefs, "hizmet", "ürün", "urun", "çözüm", "cozum", "product", "service", "faaliyet"):
        s = 8 if words > 400 else 6
        w = "hizmet/ürün bölümü mevcut"
    else:
        s, w = 3, "ayrı hizmet/ürün bölümü bulunamadı"
    br.append(("Hizmetlerin sunumu", s, w))

    # 6. References / projects (10)
    if _has(nav + hrefs, "referans", "proje", "project", "reference", "galeri", "uygulama"):
        r = 8; w = "referans/proje bölümü mevcut"
    else:
        r = 2; w = "referans veya proje sayfası yok"
    br.append(("Referans ve proje sunumu", r, w))

    # 7. SEO & technical (10)
    t = 0
    why = []
    if a.get("https"):
        t += 3; why.append("HTTPS")
    else:
        why.append("HTTPS yok")
    if a.get("title") and len(a.get("title")) > 10:
        t += 2
    else:
        why.append("başlık etiketi zayıf")
    if a.get("meta_desc"):
        t += 2
    else:
        why.append("meta açıklama yok")
    if "schema" in tech or "OpenGraph" in tech:
        t += 1
    if a.get("lang_en"):
        t += 2; why.append("İngilizce sürüm var")
    else:
        why.append("İngilizce sürüm yok")
    br.append(("SEO ve teknik durum", t, ", ".join(why)))

    # 8. Contact & conversion (5)
    k = 0
    why = []
    if a.get("emails_on_domain"):
        k += 2; why.append("kurumsal e-posta yayında")
    elif a.get("emails"):
        k += 1; why.append("e-posta var (kurumsal alan adı değil)")
    if a.get("phones"):
        k += 1
    if a.get("form_count", 0) > 0:
        k += 1; why.append("form var")
    if "WhatsApp" in tech:
        k += 1; why.append("WhatsApp")
    k = min(5, k)
    br.append(("İletişim ve dönüşüm", k, ", ".join(why) or "zayıf"))

    total = sum(x[1] for x in br)
    if total >= 75:
        st = "D"
    elif total >= 60:
        st = "C"
    else:
        st = "B"
    # Very old / non-mobile sites are B (eski) regardless
    if not a.get("viewport") or (yr and yr <= CUR_YEAR - 5):
        st = "B" if total < 75 else "C"
    if vis:
        g = vis["grade"]
        st = "B" if g <= 2 else ("C" if g == 3 and total < 80 else ("D" if g >= 4 else st))
        if g == 1 and any(k in vis["note"].lower() for k in ("çalışmıyor", "açılmadı", "park", "hata sayfası", "yayında değil")):
            st = "B"
    return total, br, st


SIZE_KEYS = {
    "imalat": ("üretim/imalat yapıyor", 5), "üretim": ("üretim/imalat yapıyor", 0), "fabrika": ("fabrika/üretim tesisi", 3),
    "anahtar teslim": ("anahtar teslim proje", 4), "taahhüt": ("taahhüt", 2), "epc": ("EPC", 2),
    "ihracat": ("ihracat", 3), "export": ("ihracat", 3), "yurt dışı": ("yurt dışı iş", 2), "yurtdışı": ("yurt dışı iş", 2),
    "iso 9001": ("ISO 9001", 1), "osb": ("OSB bağlantısı", 1), "mühendis": ("mühendislik kadrosu", 1),
    "belediye": ("kamu/belediye işleri", 2), "referans": ("referans listesi", 1),
}


VIS_NEED = {1: 28, 2: 23, 3: 13, 4: 6, 5: 2}


def potential(lead, a, ws, wstat, vis=None):
    br = []
    # Web need (30)
    if wstat == "A":
        n, w = 28, "Web sitesi bulunamadı (çoklu kaynak kontrolü gerekli)"
    elif wstat == "U":
        n, w = 20, "Siteye erişilemedi; teknik sorun büyük ihtimalle müşteri kaybettiriyor (doğrulanmalı)"
    else:
        n = round(30 * (100 - ws) / 100 * 1.25)
        n = max(0, min(30, n))
        w = f"Web sitesi puanı {ws}/100"
        if vis:
            n = max(n, VIS_NEED[vis["grade"]]) if vis["grade"] <= 3 else min(n, VIS_NEED[vis["grade"]] + 4)
            w += f"; görsel inceleme {vis['grade']}/5"
    br.append(("Web sitesi ihtiyacı", n, w))

    text = " ".join([lead.get("desc", ""), (a or {}).get("home_text", ""), " ".join((a or {}).get("nav", []))]).lower()
    # Corporate size (20)
    sz = 6
    why = []
    seen = set()
    for k, (lbl, pts) in SIZE_KEYS.items():
        if k in text and lbl not in seen:
            sz += pts; seen.add(lbl); why.append(lbl)
    m = re.search(r"(19[6-9]\d|20[0-2]\d)\s*(?:yılında|yılından|'?den beri|’den beri|since)", text)
    if m and int(m.group(1)) <= 2010:
        sz += 2; why.append(f"köklü ({m.group(1)})")
    sz = min(20, sz + lead.get("size_adj", 0))
    br.append(("Kurumsal büyüklük", sz, ", ".join(why) or "sınırlı bilgi"))

    # Commercial potential (20)
    sub = (lead.get("subsector", "") + " " + text).lower()
    if any(k in sub for k in ("epc", "anahtar teslim", "taahhüt", "imalat", "üretici", "tesis")):
        cp, w = 16, "proje/ekipman bazlı B2B iş modeli; 40.000 TL yatırım ölçeğine uygun"
    elif any(k in sub for k in ("danışman", "laboratuvar", "ölçüm", "lab")):
        cp, w = 13, "B2B hizmet şirketi; kurumsal görünüm satışı doğrudan etkiliyor"
    elif any(k in sub for k in ("atık", "geri dönüşüm", "kimya")):
        cp, w = 13, "sanayiye hizmet veren B2B firma"
    else:
        cp, w = 8, "ağırlıklı perakende/servis (ev tipi cihaz) — bütçe sınırlı olabilir"
    cp = min(20, cp + lead.get("comm_adj", 0))
    br.append(("Ticari potansiyel", cp, w))

    # Digital opportunity (15)
    do = 4
    why = []
    if a and a.get("reachable"):
        if not a.get("lang_en"):
            do += 4; why.append("İngilizce içerik yok")
        nav = " ".join(a.get("nav", []) + a.get("hrefs", [])).lower()
        if not any(k in nav for k in ("referans", "proje", "project")):
            do += 3; why.append("proje/referans portföyü yok")
        if not a.get("meta_desc"):
            do += 2; why.append("temel SEO eksik")
        if not a.get("social"):
            do += 2; why.append("sosyal medya bağlantısı yok")
    else:
        do = 13; why.append("sıfırdan dijital kimlik kurulabilir")
    do = min(15, do)
    br.append(("Dijital gelişim fırsatı", do, ", ".join(why) or "sınırlı"))

    # Contact (15)
    em = lead.get("email", "")
    est = lead.get("email_status", "")
    ct = 0
    why = []
    if em and est.startswith("Doğrulanmış"):
        ct += 10; why.append("doğrulanmış kurumsal e-posta")
    elif em and est == "Güvenilir kaynak":
        ct += 7; why.append("e-posta güvenilir kaynaktan")
    elif em:
        ct += 3; why.append("e-posta doğrulanmadı")
    if lead.get("phone"):
        ct += 3; why.append("telefon")
    if lead.get("address"):
        ct += 2; why.append("adres")
    ct = min(15, ct)
    br.append(("İletişim bilgileri", ct, ", ".join(why) or "yok"))
    total = sum(x[1] for x in br)
    cat = "A+" if total >= 85 else "A" if total >= 70 else "B" if total >= 50 else "C"
    return total, br, cat
