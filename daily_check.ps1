# 1. In den Arbeitsordner wechseln
Set-Location "C:\Workspace LM studio"

Write-Host "
=== 1. AKTUELLES VERZEICHNIS ===" -ForegroundColor Cyan
Get-Location
Write-Host "
=== 2. ORDNERINHALT ===" -ForegroundColor Cyan
Get-ChildItem -Name
Write-Host "
=== 3. GIT STATUS ===" -ForegroundColor Cyang
git status
if (!(Test-Path C:\Users\Pascal\OneDrive\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1)) { New-Item -Type File -Path C:\Users\Pascal\OneDrive\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1 -Force }; Add-Content -Path C:\Users\Pascal\OneDrive\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1 -Value 'function daily { & "C:\Workspace LM studio\daily_check.ps1" }'
