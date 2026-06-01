# run.ps1 - convenience runner for the Locust load test.
# Authorized targets only.
#
# Examples:
#   .\run.ps1 -Host https://target.example.com                 # opens web UI on :8089
#   .\run.ps1 -Host https://target.example.com -Headless -Users 500 -Rate 50 -Time 5m
#   .\run.ps1 -Host https://target.example.com -Master         # distributed master
#   .\run.ps1 -MasterHost 10.0.0.5 -Worker                     # a worker on another box

param(
    [string]$Host_      = "",
    [switch]$Headless,
    [int]$Users         = 100,
    [int]$Rate          = 10,        # users spawned per second
    [string]$Time       = "5m",
    [switch]$Master,
    [switch]$Worker,
    [string]$MasterHost = "127.0.0.1",
    [switch]$Insecure
)

# Resolve locust executable (global or venv)
$locust = (Get-Command locust -ErrorAction SilentlyContinue).Source
if (-not $locust -and (Test-Path "$PSScriptRoot\.venv\Scripts\locust.exe")) {
    $locust = "$PSScriptRoot\.venv\Scripts\locust.exe"
}
if (-not $locust) {
    Write-Host "Locust not installed. Run .\setup.ps1 first." -ForegroundColor Yellow
    exit 1
}

$f = "$PSScriptRoot\locustfile.py"
$cliArgs = @("-f", $f)

if ($Worker) {
    $cliArgs += @("--worker", "--master-host", $MasterHost)
}
else {
    if (-not $Host_) { Write-Host "Provide -Host <url>" -ForegroundColor Yellow; exit 1 }
    $cliArgs += @("--host", $Host_)
    Write-Host "Load testing $Host_ - authorized targets only." -ForegroundColor Green
    if ($Master)   { $cliArgs += "--master" }
    if ($Headless) { $cliArgs += @("--headless", "-u", $Users, "-r", $Rate, "-t", $Time, "--csv", "results") }
    if ($Insecure) { $cliArgs += "--tls-cert-verify=false" }
}

& $locust @cliArgs
