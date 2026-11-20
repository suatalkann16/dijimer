#!/usr/bin/env python3
"""Dalga 1 e-postalarından Outlook'ta açılacak .eml taslakları, inceleme dosyası ve CSV üretir.

.eml dosyalarında 'X-Unsent: 1' başlığı var: Outlook (Windows masaüstü) dosyayı açınca
gönderilmemiş, düzenlenebilir yeni bir e-posta olarak açar. Hiçbir şey otomatik gönderilmez.
"""
import csv, html, os, re, sys, unicodedata
from email.message import EmailMessage
from email.policy import SMTP
sys.path.insert(0, os.path.dirname(__file__))
from epostalar import EPOSTALAR, ORTAK_KAPANIS

GONDEREN = "Dijimer Bilişim <info@dijimerbilisim.com>"
CIKIS = ("Bu e-postayı firmanızın web sitesinde yayımlanan kurumsal iletişim adresine gönderdik. "
         "Tekrar e-posta almak istemezseniz “Çıkar” yazarak yanıtlamanız yeterli.")
D = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(D, "eml"), exist_ok=True)


def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("ı", "i").replace("İ", "I")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:40]


def strip_tags(s):
    return re.sub(r"<a href=\"([^\"]+)\">[^<]+</a>", r"\1", s)


inceleme = ["# Dalga 1 – Gönderime hazır e-postalar (20 firma)\n",
            "> Hiçbiri gönderilmedi. Her e-postayı Outlook'ta açıp okuyun, imzanızı ekleyip kendiniz gönderin.\n"]
rows = []
for e in EPOSTALAR:
    paras = list(e["p"]) + ([ORTAK_KAPANIS] if e.get("kapanis", True) else [])
    p_html = "".join(f"<p style=\"margin:0 0 12px\">{x if '<a ' in x else html.escape(x)}</p>" for x in paras)
    body_html = (
        "<html><body style=\"margin:0;font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#222\">"
        "<table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"600\" style=\"max-width:600px\">"
        "<tr><td style=\"border-top:4px solid #E53935;padding:18px 0 0 0\">"
        f"<p style=\"margin:0 0 12px\">{html.escape(e['selam'])}</p>{p_html}"
        "<p style=\"margin:0 0 4px\">Saygılarımla,</p><p style=\"margin:0 0 18px\">&nbsp;</p>"
        "</td></tr><tr><td style=\"border-top:1px solid #E6E7EA;padding:10px 0 0 0\">"
        f"<p style=\"margin:0;font-size:8.5pt;color:#888\">{html.escape(CIKIS)}</p>"
        "</td></tr></table></body></html>")
    body_txt = "\n\n".join([e["selam"]] + [strip_tags(x) for x in paras] + ["Saygılarımla,", "", CIKIS])

    m = EmailMessage(policy=SMTP)
    m["From"] = GONDEREN
    m["To"] = e["alici"]
    m["Subject"] = e["konu"]
    m["X-Unsent"] = "1"
    m.set_content(body_txt)
    m.add_alternative(body_html, subtype="html")
    fn = f"{e['id']}-{slug(e['firma'])}.eml"
    open(os.path.join(D, "eml", fn), "wb").write(bytes(m))

    rows.append({"No": e["id"], "Firma": e["firma"], "Kime": e["alici"], "Konu": e["konu"], "Dosya": fn,
                 "Metin": body_txt, "Gönderildi mi": "", "Gönderim tarihi": "", "Yanıt": ""})
    inceleme += [f"\n---\n\n## {e['id']}. {e['firma']}\n", f"- **Kime:** {e['alici']}", f"- **Konu:** {e['konu']}",
                 f"- **Outlook dosyası:** `eml/{fn}`\n", "```text", body_txt, "```"]

open(os.path.join(D, "INCELEME.md"), "w", encoding="utf-8").write("\n".join(inceleme) + "\n")
with open(os.path.join(D, "gonderim_listesi.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(rows)
print(len(rows), "e-posta hazır:", os.path.join(D, "eml"))
