# Check GitHub Actions Build Status
Write-Host "`n=== Load Tester Android - Build Status ===" -ForegroundColor Cyan
Write-Host ""

# GitHub repo info
$repo = "Gabriel-C33/loadtester-android"
$actionsUrl = "https://github.com/$repo/actions"
$releasesUrl = "https://github.com/$repo/releases"

Write-Host "Repository: " -NoNewline
Write-Host $repo -ForegroundColor Yellow

Write-Host "`nBuild Status: " -NoNewline
Write-Host $actionsUrl -ForegroundColor Green

Write-Host "`nReleases: " -NoNewline
Write-Host $releasesUrl -ForegroundColor Green

Write-Host "`n--- What to do next ---" -ForegroundColor Cyan
Write-Host "1. Open Actions URL to check build progress"
Write-Host "2. Wait for build to complete (15-30 minutes)"
Write-Host "3. Download APK from Releases page"
Write-Host "4. Install on your Android phone"
Write-Host ""

# Check if local APK exists
if (Test-Path "bin/*.apk") {
    Write-Host "Local APK found:" -ForegroundColor Green
    Get-ChildItem bin/*.apk | ForEach-Object {
        $sizeMB = [math]::Round($_.Length/1MB, 2)
        Write-Host "  $($_.Name) - $sizeMB MB" -ForegroundColor Cyan
    }
    Write-Host "`nYou can install this APK on your phone now!" -ForegroundColor Yellow
    Write-Host "Command: adb install bin/$((Get-ChildItem bin/*.apk)[0].Name)" -ForegroundColor Gray
} else {
    Write-Host "No local APK found. Waiting for GitHub Actions build..." -ForegroundColor Yellow
}

Write-Host "`n===========================================`n" -ForegroundColor Cyan
