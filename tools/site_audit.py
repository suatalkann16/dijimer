#!/usr/bin/env python3
"""Dijimer lead research - technical website audit.

Usage: python3 tools/site_audit.py <url> [<url> ...]  -> prints JSON per site
Collects objective signals used by the 100-point website score:
reachability, HTTPS, mobile viewport, title/meta description, copyright year,
CMS/generator, page weight, image count, language links, emails/phones found
on the homepage and on a contact page (only addresses actually published).
"""
import json, re, sys, time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?90[\s\-]?)?\(?0?\s?[2-5]\d{2}\)?[\s\-.]?\d{3}[\s\-.]?\d{2}[\s\-.]?\d{2}")
YEAR_RE = re.compile(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(\d{4})", re.I)
CONTACT_HINTS = ("iletisim", "iletişim", "contact", "bize-ulasin", "ulasim")
BAD_EMAIL_PARTS = ("example.", "sentry", "wixpress", "@2x", ".png", ".jpg", ".webp", "domain.com", "yourmail", "email.com")


def get(url, timeout=20):
    resp = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "tr,en"}, timeout=timeout, allow_redirects=True)
    if (resp.encoding or "").lower() in ("iso-8859-1", ""):
        m = re.search(rb'charset=["\']?([A-Za-z0-9_-]+)', resp.content[:3000])
        resp.encoding = m.group(1).decode() if m else (resp.apparent_encoding or "utf-8")
    return resp


def _cf(h):
    try:
        k = int(h[:2], 16)
        return "".join(chr(int(h[i:i + 2], 16) ^ k) for i in range(2, len(h), 2))
    except Exception:
        return ""


def clean_emails(text):
    out = set()
    # Cloudflare email obfuscation (data-cfemail / /cdn-cgi/l/email-protection#...)
    for h in re.findall(r'data-cfemail="([0-9a-fA-F]+)"', text) + re.findall(r'email-protection#([0-9a-fA-F]+)', text):
        d = _cf(h)
        if "@" in d:
            text += " " + d
    for e in EMAIL_RE.findall(text):
        e = e.strip(".").lower()
        if not any(b in e for b in BAD_EMAIL_PARTS):
            out.add(e)
    return out


def audit(url):
    host = re.sub(r"^https?://", "", url).strip("/")
    r = {"input": url, "checked_at": time.strftime("%Y-%m-%d")}
    resp = None
    errs = []
    cands = [f"https://{host}"]
    if not host.startswith("www."):
        cands.append(f"https://www.{host}")
    else:
        cands.append(f"https://{host[4:]}")
    for cand in cands:
        try:
            t0 = time.time()
            resp = get(cand)
            r["load_s"] = round(time.time() - t0, 2)
            break
        except requests.exceptions.SSLError as ex:
            errs.append("SSL_ERROR " + cand)
            r["ssl_error"] = True
        except Exception as ex:
            errs.append(type(ex).__name__ + " " + cand + ": " + str(ex)[:80])
    if resp is None:
        r["reachable"] = False
        r["error"] = " | ".join(errs)
        return r
    r["reachable"] = resp.ok
    r["status"] = resp.status_code
    r["final_url"] = resp.url
    r["https"] = resp.url.startswith("https")
    html = resp.text
    r["html_kb"] = round(len(resp.content) / 1024, 1)
    soup = BeautifulSoup(html, "lxml")
    vp = soup.find("meta", attrs={"name": re.compile("^viewport$", re.I)})
    r["viewport"] = bool(vp)
    r["title"] = (soup.title.string or "").strip()[:120] if soup.title and soup.title.string else ""
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    r["meta_desc"] = (md.get("content") or "").strip()[:160] if md else ""
    gen = soup.find("meta", attrs={"name": re.compile("^generator$", re.I)})
    r["generator"] = gen.get("content", "")[:60] if gen else ""
    low = html.lower()
    tech = []
    for key, name in [("wp-content", "WordPress"), ("wix.com", "Wix"), ("joomla", "Joomla"), ("jquery", "jQuery"),
                      ("bootstrap", "Bootstrap"), ("elementor", "Elementor"), ("flash", "Flash?"), ("<table", "table-layout?"),
                      ("frameset", "frameset"), ("marquee", "marquee"), ("google-analytics", "GA"), ("gtag(", "gtag"),
                      ("schema.org", "schema"), ("og:title", "OpenGraph"), ("whatsapp", "WhatsApp"), ("recaptcha", "form-recaptcha"),
                      ("tailwind", "Tailwind"), ("react-dom", "React"), ("_next/", "Next.js"), ("shopify", "Shopify"), ("myikas", "ikas"),
                      ("ticimax.com", "Ticimax"), ("ideasoft.com", "IdeaSoft")]:
        if key in low:
            tech.append(name)
    r["tech"] = tech
    years = [int(y) for y in YEAR_RE.findall(html) if 1995 < int(y) < 2030]
    r["copyright_year"] = max(years) if years else None
    r["img_count"] = len(soup.find_all("img"))
    r["form_count"] = len(soup.find_all("form"))
    text = soup.get_text(" ", strip=True)
    r["text_words"] = len(text.split())
    links = [a.get("href", "") for a in soup.find_all("a")]
    r["link_count"] = len(links)
    navt = []
    for a in soup.find_all("a"):
        t = a.get_text(" ", strip=True).lower()[:40]
        if t and t not in navt:
            navt.append(t)
    r["nav"] = navt[:120]
    r["hrefs"] = list(dict.fromkeys(l for l in links if l))[:150]
    r["lang_en"] = any(re.search(r"(/en/|/en$|lang=en|english|/eng)", l or "", re.I) for l in links)
    socials = {}
    for l in links:
        for s in ("linkedin.com", "instagram.com", "facebook.com", "youtube.com", "twitter.com", "x.com/"):
            if l and s in l and s not in socials:
                socials[s.split(".")[0].replace("/", "")] = l[:120]
    r["social"] = socials
    emails = clean_emails(html)
    phones = set(p.strip() for p in PHONE_RE.findall(text))
    # contact page
    contact = None
    for a in soup.find_all("a"):
        h = (a.get("href") or "").lower()
        if any(c in h for c in CONTACT_HINTS):
            contact = urljoin(resp.url, a.get("href"))
            break
    r["contact_page"] = contact
    if contact:
        try:
            c = get(contact, timeout=15)
            emails |= clean_emails(c.text)
            ct = BeautifulSoup(c.text, "lxml").get_text(" ", strip=True)
            phones |= set(p.strip() for p in PHONE_RE.findall(ct))
            r["contact_text"] = ct[:600]
        except Exception:
            pass
    dom = urlparse(resp.url).netloc.replace("www.", "")
    r["emails"] = sorted(emails)
    r["emails_on_domain"] = sorted(e for e in emails if e.split("@")[1].endswith(dom.split(":")[0]))
    r["phones"] = sorted(phones)[:6]
    r["home_text"] = text[:900]
    return r


if __name__ == "__main__":
    out = []
    for u in sys.argv[1:]:
        out.append(audit(u))
    print(json.dumps(out, ensure_ascii=False, indent=1))
