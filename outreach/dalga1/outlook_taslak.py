#!/usr/bin/env python3
"""Dalga 1 e-postalarını Outlook'ta (klasik, Windows) Taslaklar klasörüne yazan PowerShell betiği üretir.

Çıktı: outreach/dalga1/outlook/taslaklari-olustur.ps1 + TASLAKLARI-OLUSTUR.bat
Betik e-posta GÖNDERMEZ; yalnızca taslak kaydeder. Varsayılan imza (DİJİMER) Outlook tarafından eklenir.
"""
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from epostalar import EPOSTALAR, ORTAK_KAPANIS

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "outlook")
os.makedirs(OUT, exist_ok=True)
HESAP = "info@dijimerbilisim.com"
CIKIS = ("Bu e-postayı firmanızın web sitesinde yayımlanan kurumsal iletişim adresine gönderdik. "
         "Tekrar e-posta almak istemezseniz “Çıkar” yazarak yanıtlamanız yeterli.")
STYLE = "font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#222222;margin:0 0 11pt 0"


def para(x):
    return f'<p style="{STYLE}">{x if "<a " in x else html.escape(x)}</p>'


def govde(e):
    ps = list(e["p"]) + ([ORTAK_KAPANIS] if e.get("kapanis", True) else [])
    return para(e["selam"]) + "".join(para(x) for x in ps) + para("Saygılarımla,")


def ps_str(s):  # PowerShell tek tırnaklı dize
    return "'" + s.replace("'", "''") + "'"


kalemler = []
for e in EPOSTALAR:
    kalemler.append("  @{ No=%s; Kime=%s; Konu=%s; Govde=%s }" % (
        ps_str(e["id"]), ps_str(e["alici"]), ps_str(e["konu"]), ps_str(govde(e))))

ps1 = r"""# Dijimer Bilişim – Dalga 1 Outlook taslakları
# Bu betik e-posta GÖNDERMEZ. Yalnızca Outlook'ta Taslaklar klasörüne 20 taslak kaydeder.
# Gereken: klasik Outlook (Windows) açık olmalı; "Yeni iletiler" için varsayılan imza DİJİMER seçili olmalı.

$ErrorActionPreference = 'Stop'
$Hesap = '__HESAP__'
$Cikis = __CIKIS__

$Liste = @(
__KALEMLER__
)

Write-Host ''
Write-Host 'Dijimer Bilisim - Outlook taslak olusturucu' -ForegroundColor Red
Write-Host ("{0} e-posta Taslaklar klasorune kaydedilecek. HICBIRI GONDERILMEYECEK." -f $Liste.Count)
$cevap = Read-Host 'Devam edilsin mi? (E/H)'
if ($cevap -notin @('E','e')) { Write-Host 'Iptal edildi.'; exit }

try { $ol = [Runtime.InteropServices.Marshal]::GetActiveObject('Outlook.Application') }
catch { $ol = New-Object -ComObject Outlook.Application }

$hesapObj = $null
foreach ($a in $ol.Session.Accounts) { if ($a.SmtpAddress -ieq $Hesap) { $hesapObj = $a } }
if (-not $hesapObj) { Write-Host "UYARI: $Hesap hesabi bulunamadi; varsayilan hesap kullanilacak." -ForegroundColor Yellow }

$imzaUyarisi = $false
$sayac = 0
foreach ($m in $Liste) {
  $mail = $ol.CreateItem(0)
  if ($hesapObj) { $mail.SendUsingAccount = $hesapObj }
  $mail.To = $m.Kime
  $mail.Subject = $m.Konu
  $null = $mail.GetInspector            # Outlook varsayilan imzayi (DIJIMER) bu adimda ekler
  $h = $mail.HTMLBody
  if ($h -notmatch '_MailAutoSig') { $imzaUyarisi = $true }
  $cikisHtml = '<p style="font-family:Calibri,Arial,sans-serif;font-size:8.5pt;color:#888888;margin:14pt 0 0 0">' + $Cikis + '</p>'
  $i = $h.IndexOf('<body', [StringComparison]::OrdinalIgnoreCase)
  if ($i -ge 0) {
    $j = $h.IndexOf('>', $i) + 1
    $h = $h.Substring(0, $j) + $m.Govde + $h.Substring($j)
    $k = $h.LastIndexOf('</body>', [StringComparison]::OrdinalIgnoreCase)
    if ($k -ge 0) { $h = $h.Substring(0, $k) + $cikisHtml + $h.Substring($k) }
  } else { $h = $m.Govde + $h + $cikisHtml }
  $mail.HTMLBody = $h
  $mail.Save()
  $sayac++
  Write-Host ("  [{0}] {1}  ->  {2}" -f $m.No, $m.Kime, 'taslak kaydedildi') -ForegroundColor Green
}

Write-Host ''
Write-Host ("Tamamlandi: {0} taslak Outlook > Taslaklar klasorunde." -f $sayac) -ForegroundColor Green
if ($imzaUyarisi) {
  Write-Host 'UYARI: Imza eklenmedi. Outlook > Dosya > Secenekler > Posta > Imzalar > "Yeni iletiler" alanini DIJIMER yapin,' -ForegroundColor Yellow
  Write-Host '       Taslaklar klasorundeki bu 20 taslagi silip betigi yeniden calistirin.' -ForegroundColor Yellow
}
Write-Host 'Simdi Taslaklar klasorunu acin, her e-postayi okuyup Gonder''e basin. Gunde 5-8 e-posta onerilir.'
""".replace("__HESAP__", HESAP).replace("__CIKIS__", ps_str(CIKIS)).replace("__KALEMLER__", "\n".join(kalemler))

# Windows PowerShell 5.1 için UTF-8 BOM şart
open(os.path.join(OUT, "taslaklari-olustur.ps1"), "w", encoding="utf-8-sig", newline="\r\n").write(ps1)
bat = ('@echo off\r\nchcp 65001 >nul\r\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0taslaklari-olustur.ps1"\r\n'
       'echo.\r\npause\r\n')
open(os.path.join(OUT, "TASLAKLARI-OLUSTUR.bat"), "w", encoding="ascii", newline="").write(bat)
print("hazır:", OUT, len(kalemler), "taslak")
