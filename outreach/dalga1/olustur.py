#!/usr/bin/env python3
"""Dalga 1 e-postalarından Dijimer kurumsal HTML şablonlu Outlook .eml taslakları üretir.

- 'X-Unsent: 1' başlığı: Outlook (Windows masaüstü) dosyayı gönderilmemiş, düzenlenebilir
  yeni e-posta olarak açar. Hiçbir şey otomatik gönderilmez.
- Logo e-postanın içine gömülüdür (cid); internetten resim çekmez.
- İmza ve iletişim bilgileri şablonun içindedir; ayrıca imza eklemeye gerek yoktur.
"""
import csv, html, os, re, sys, unicodedata
from email.message import EmailMessage
from email.policy import SMTP
sys.path.insert(0, os.path.dirname(__file__))
from epostalar import EPOSTALAR, ORTAK_KAPANIS

D = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(D, "..", "dijimer-logo-eposta.png")
GONDEREN = "Dijimer Bilişim <info@dijimerbilisim.com>"
PAKET_URL = "https://dijimerbilisim.com/kurumsal-web-sitesi"
CIKIS = ("Bu e-postayı firmanızın web sitesinde yayımlanan kurumsal iletişim adresine gönderdik. "
         "Tekrar e-posta almak istemezseniz “Çıkar” yazarak yanıtlamanız yeterli.")

# Marka
RED, INK, TEXT, MUTED, BORDER, SOFT, BG = "#E53935", "#0F1115", "#3F444B", "#5B616B", "#E6E7EA", "#FDECEA", "#F2F3F5"
FONT = "'Segoe UI',Arial,Helvetica,sans-serif"

os.makedirs(os.path.join(D, "eml"), exist_ok=True)


def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("ı", "i").replace("İ", "I")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:40]


def strip_tags(s):
    return re.sub(r"<a href=\"([^\"]+)\">[^<]+</a>", r"\1", s)


def esc(x):
    return x if "<a " in x else html.escape(x)


def P(x, extra=""):
    return f'<p style="margin:0 0 14px;font-family:{FONT};font-size:15px;line-height:23px;color:{TEXT};{extra}">{esc(x)}</p>'


def sablon(e):
    giris, gozlem, diger = e["p"][0], e["p"][1], e["p"][2:]
    kapanis = ORTAK_KAPANIS.split(" Paket içeriğini")[0] + " Uygun görürseniz ihtiyacınızı kısa bir görüşmede dinleyip size özel teklifimizi iletelim." if e.get("kapanis", True) else ""
    dugme = e.get("kapanis", True)
    kutu_baslik = e.get("kutu_baslik", "Gözümüze çarpan")
    return f"""<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"></head>
<body style="margin:0;padding:0;background:{BG};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{BG}" style="background:{BG};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;" bgcolor="#FFFFFF">
  <tr><td height="5" bgcolor="{RED}" style="background:{RED};font-size:0;line-height:0;">&nbsp;</td></tr>
  <tr><td align="left" style="padding:24px 28px 16px;border-bottom:1px solid {BORDER};">
    <img src="cid:dijimerlogo" width="157" height="40" alt="Dijimer Bilişim" style="display:block;border:0;width:157px;height:40px;">
  </td></tr>
  <tr><td style="padding:28px 28px 8px;">
    <p style="margin:0 0 18px;font-family:{FONT};font-size:15px;line-height:23px;color:{INK};font-weight:600;">{html.escape(e['selam'])}</p>
    {P(giris)}
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 18px;">
      <tr><td width="4" bgcolor="{RED}" style="background:{RED};">&nbsp;</td>
      <td bgcolor="{SOFT}" style="background:{SOFT};padding:16px 18px;">
        <p style="margin:0 0 6px;font-family:{FONT};font-size:12px;letter-spacing:.6px;text-transform:uppercase;color:{RED};font-weight:700;">{html.escape(kutu_baslik)}</p>
        <p style="margin:0;font-family:{FONT};font-size:15px;line-height:23px;color:{INK};">{esc(gozlem)}</p>
      </td></tr>
    </table>
    {''.join(P(x) for x in diger)}
    {P(kapanis) if kapanis else ''}
  </td></tr>
  {f'''<tr><td style="padding:4px 28px 26px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
      <td bgcolor="{RED}" style="background:{RED};border-radius:6px;">
        <a href="{PAKET_URL}" style="display:inline-block;padding:12px 22px;font-family:{FONT};font-size:14px;font-weight:600;color:#FFFFFF;text-decoration:none;">Paket içeriğini inceleyin &rarr;</a>
      </td></tr></table>
  </td></tr>''' if dugme else ''}
  <tr><td style="padding:6px 28px 28px;">
    <p style="margin:0 0 2px;font-family:{FONT};font-size:15px;line-height:23px;color:{TEXT};">Saygılarımla,</p>
    <p style="margin:0;font-family:{FONT};font-size:15px;line-height:23px;color:{INK};font-weight:700;">Dijimer Bilişim</p>
    <p style="margin:0;font-family:{FONT};font-size:13px;line-height:20px;color:{MUTED};">Yazılım ve Dijital Çözümler · Bursa</p>
  </td></tr>
  <tr><td bgcolor="{INK}" style="background:{INK};padding:18px 28px;">
    <p style="margin:0;font-family:{FONT};font-size:13px;line-height:21px;color:#FFFFFF;">
      <a href="tel:+905383701179" style="color:#FFFFFF;text-decoration:none;">0538 370 11 79</a> &nbsp;·&nbsp;
      <a href="mailto:info@dijimerbilisim.com" style="color:#FFFFFF;text-decoration:none;">info@dijimerbilisim.com</a> &nbsp;·&nbsp;
      <a href="https://dijimerbilisim.com" style="color:#FFFFFF;text-decoration:none;">dijimerbilisim.com</a></p>
  </td></tr>
</table>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;"><tr><td style="padding:14px 28px 0;">
  <p style="margin:0;font-family:{FONT};font-size:11px;line-height:17px;color:#8A9099;">{html.escape(CIKIS)}</p>
</td></tr></table>
</td></tr></table></body></html>"""


inceleme = ["# Dalga 1 – Gönderime hazır e-postalar (20 firma)\n",
            "> Hiçbiri gönderilmedi. Her e-postayı Outlook'ta açıp okuyun ve kendiniz gönderin. İmza şablonun içinde.\n"]
rows = []
logo = open(LOGO, "rb").read()
for e in EPOSTALAR:
    paras = list(e["p"]) + ([ORTAK_KAPANIS] if e.get("kapanis", True) else [])
    body_txt = "\n\n".join([e["selam"]] + [strip_tags(x) for x in paras] +
                           ["Saygılarımla,\nDijimer Bilişim\n0538 370 11 79 · info@dijimerbilisim.com · dijimerbilisim.com", CIKIS])
    m = EmailMessage(policy=SMTP)
    m["From"] = GONDEREN
    m["To"] = e["alici"]
    m["Subject"] = e["konu"]
    m["X-Unsent"] = "1"
    m.set_content(body_txt)
    m.add_alternative(sablon(e), subtype="html")
    m.get_payload()[1].add_related(logo, maintype="image", subtype="png", cid="<dijimerlogo>", filename="dijimer-logo.png")
    fn = f"{e['id']}-{slug(e['firma'])}.eml"
    open(os.path.join(D, "eml", fn), "wb").write(bytes(m))
    if e["id"] == "06":
        open(os.path.join(D, "ornek.html"), "w", encoding="utf-8").write(sablon(e).replace("cid:dijimerlogo", "../dijimer-logo-eposta.png"))
    rows.append({"No": e["id"], "Firma": e["firma"], "Kime": e["alici"], "Konu": e["konu"], "Dosya": fn,
                 "Metin": body_txt, "Gönderildi mi": "", "Gönderim tarihi": "", "Yanıt": ""})
    inceleme += [f"\n---\n\n## {e['id']}. {e['firma']}\n", f"- **Kime:** {e['alici']}", f"- **Konu:** {e['konu']}",
                 f"- **Outlook dosyası:** `eml/{fn}`\n", "```text", body_txt, "```"]

open(os.path.join(D, "INCELEME.md"), "w", encoding="utf-8").write("\n".join(inceleme) + "\n")
with open(os.path.join(D, "gonderim_listesi.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(rows)
print(len(rows), "e-posta hazır:", os.path.join(D, "eml"))
