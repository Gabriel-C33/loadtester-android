# setup.ps1 — one-time setup: installs Python (if needed) + Locust in a venv.

# 1. Ensure Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Installing via winget..." -ForegroundColor Cyan
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    Write-Host "Python installed. CLOSE and REOPEN this terminal, then run setup.ps1 again." -ForegroundColor Yellow
    exit 0
}

# 2. Create venv + install locust
Push-Location $PSScriptRoot
python -m venv .venv
& "$PSScriptRoot\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$PSScriptRoot\.venv\Scripts\pip.exe" install -r requirements.txt
Pop-Location

Write-Host "`nDone. Now run:" -ForegroundColor Green
Write-Host '  .\run.ps1 -Host https://target.example.com' -ForegroundColor Cyan
