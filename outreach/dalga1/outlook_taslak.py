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

# 1) info@ hesabini bul (bulamazsa DUR - baska hesaba kaydetme)
$hesapObj = $null
foreach ($a in $ol.Session.Accounts) {
  if ($a.SmtpAddress -ieq $Hesap -or $a.DisplayName -like '*dijimerbilisim*' -or $a.UserName -ieq $Hesap) { $hesapObj = $a }
}
if (-not $hesapObj) {
  Write-Host "HATA: Outlook'ta $Hesap hesabi bulunamadi. Hicbir taslak olusturulmadi." -ForegroundColor Red
  Write-Host 'Outlook daki hesaplar:'
  foreach ($a in $ol.Session.Accounts) { Write-Host ("  - {0}  ({1})" -f $a.DisplayName, $a.SmtpAddress) }
  exit
}
Write-Host ("Hesap: {0}" -f $hesapObj.SmtpAddress) -ForegroundColor Cyan

# 2) Bu hesabin KENDI Taslaklar klasoru
$taslakKlasoru = $null
try { $taslakKlasoru = $hesapObj.DeliveryStore.GetDefaultFolder(16) } catch {}
if (-not $taslakKlasoru) {   # IMAP hesaplarinda klasoru adindan bul
  try { foreach ($f in $hesapObj.DeliveryStore.GetRootFolder().Folders) { if ($f.Name -in @('Taslaklar','Drafts','INBOX.Drafts')) { $taslakKlasoru = $f } } } catch {}
}
if (-not $taslakKlasoru) {
  Write-Host 'HATA: Bu hesabin Taslaklar klasoru bulunamadi. Hicbir taslak olusturulmadi.' -ForegroundColor Red
  exit
}
Write-Host ("Kayit yeri: {0}" -f $taslakKlasoru.FolderPath) -ForegroundColor Cyan

# 3) Imza dosyasi (otomatik imza gelmezse kullanilir)
$imzaHtml = $null
$imzaDir = Join-Path $env:APPDATA 'Microsoft\Signatures'
$imzaDosya = Get-ChildItem -Path $imzaDir -Filter '*.htm' -ErrorAction SilentlyContinue |
  Where-Object { $_.BaseName -match '(?i)d[iıİ]j[iıİ]mer' } | Select-Object -First 1
if ($imzaDosya) {
  $raw = [System.IO.File]::ReadAllText($imzaDosya.FullName, [Text.Encoding]::Default)
  if ($raw -match '(?is)<body[^>]*>(.*)</body>') { $imzaHtml = $Matches[1] } else { $imzaHtml = $raw }
  $klasorAdi = $imzaDosya.BaseName + '_files'
  $imzaHtml = $imzaHtml -replace ('(?i)src="' + [regex]::Escape($klasorAdi) + '/'), ('src="' + (Join-Path $imzaDosya.DirectoryName $klasorAdi) + '\')
  Write-Host ("Imza dosyasi: {0}" -f $imzaDosya.Name) -ForegroundColor Cyan
} else {
  Write-Host 'Not: Signatures klasorunde DIJIMER imza dosyasi bulunamadi; Outlook un otomatik imzasi kullanilacak.' -ForegroundColor Yellow
}

# 4) Daha once olusturulmus ayni konulu taslaklari atla
$mevcut = @{}
foreach ($it in $taslakKlasoru.Items) { try { $mevcut[$it.Subject] = $true } catch {} }

$imzaUyarisi = $false
$sayac = 0
foreach ($m in $Liste) {
  if ($mevcut.ContainsKey($m.Konu)) { Write-Host ("  [{0}] {1}  ->  zaten var, atlandi" -f $m.No, $m.Kime) -ForegroundColor DarkGray; continue }
  $mail = $taslakKlasoru.Items.Add(0)
  $mail.SendUsingAccount = $hesapObj
  $mail.To = $m.Kime
  $mail.Subject = $m.Konu
  $null = $mail.GetInspector            # Outlook bu hesabin varsayilan imzasini burada ekler
  $h = $mail.HTMLBody
  $imzaVar = $h -match '_MailAutoSig'
  $ek = ''
  if (-not $imzaVar) {
    if ($imzaHtml) { $ek = $imzaHtml } else { $imzaUyarisi = $true }
  }
  $cikisHtml = '<p style="font-family:Calibri,Arial,sans-serif;font-size:8.5pt;color:#888888;margin:14pt 0 0 0">' + $Cikis + '</p>'
  $i = $h.IndexOf('<body', [StringComparison]::OrdinalIgnoreCase)
  if ($i -ge 0) {
    $j = $h.IndexOf('>', $i) + 1
    $h = $h.Substring(0, $j) + $m.Govde + $ek + $h.Substring($j)
    $k = $h.LastIndexOf('</body>', [StringComparison]::OrdinalIgnoreCase)
    if ($k -ge 0) { $h = $h.Substring(0, $k) + $cikisHtml + $h.Substring($k) }
  } else { $h = '<html><body>' + $m.Govde + $ek + $cikisHtml + '</body></html>' }
  $mail.HTMLBody = $h
  $mail.Save()
  $sayac++
  Write-Host ("  [{0}] {1}  ->  taslak kaydedildi" -f $m.No, $m.Kime) -ForegroundColor Green
}

Write-Host ''
Write-Host ("Tamamlandi: {0} yeni taslak -> {1}" -f $sayac, $taslakKlasoru.FolderPath) -ForegroundColor Green
if ($imzaUyarisi) {
  Write-Host 'UYARI: Imza eklenemedi. Outlook > Dosya > Secenekler > Posta > Imzalar: "E-posta hesabi" alaninda info@ hesabini secin,' -ForegroundColor Yellow
  Write-Host '       "Yeni iletiler" alanini DIJIMER yapin; olusan taslaklari silip betigi yeniden calistirin.' -ForegroundColor Yellow
}
Write-Host 'Simdi Taslaklar klasorunu acin, her e-postayi okuyup Gonder''e basin. Gunde 5-8 e-posta onerilir.'
""".replace("__HESAP__", HESAP).replace("__CIKIS__", ps_str(CIKIS)).replace("__KALEMLER__", "\n".join(kalemler))

# Windows PowerShell 5.1 için UTF-8 BOM şart
open(os.path.join(OUT, "taslaklari-olustur.ps1"), "w", encoding="utf-8-sig", newline="\r\n").write(ps1)
bat = ('@echo off\r\nchcp 65001 >nul\r\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0taslaklari-olustur.ps1"\r\n'
       'echo.\r\npause\r\n')
open(os.path.join(OUT, "TASLAKLARI-OLUSTUR.bat"), "w", encoding="ascii", newline="").write(bat)
print("hazır:", OUT, len(kalemler), "taslak")
