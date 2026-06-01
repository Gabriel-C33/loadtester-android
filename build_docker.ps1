# Build Android APK using Docker
Write-Host "Building Android APK using Docker..." -ForegroundColor Green

# Check if Docker is running
try {
    docker ps | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: Docker is not installed or not running." -ForegroundColor Red
    exit 1
}

# Build Docker image
Write-Host "`nBuilding Docker image..." -ForegroundColor Yellow
docker build -t loadtester-builder .

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker image build failed." -ForegroundColor Red
    exit 1
}

# Run build in container
Write-Host "`nRunning buildozer in Docker container..." -ForegroundColor Yellow
docker run --rm -v "${PWD}:/app" loadtester-builder

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: APK build failed." -ForegroundColor Red
    exit 1
}

# Check if APK was created
if (Test-Path "bin/*.apk") {
    Write-Host "`nSUCCESS! APK created:" -ForegroundColor Green
    Get-ChildItem bin/*.apk | ForEach-Object {
        Write-Host "  $($_.Name) - $([math]::Round($_.Length/1MB, 2)) MB" -ForegroundColor Cyan
    }
} else {
    Write-Host "ERROR: APK file not found in bin/ directory." -ForegroundColor Red
    exit 1
}
