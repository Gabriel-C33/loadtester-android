@echo off
echo ========================================
echo Building Android APK using Docker
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Building Docker image...
docker build -t loadtester-builder .

if %errorlevel% neq 0 (
    echo ERROR: Failed to build Docker image
    pause
    exit /b 1
)

echo.
echo Building APK (this may take 20-30 minutes on first run)...
docker run --rm -v "%cd%:/app" loadtester-builder

if %errorlevel% neq 0 (
    echo ERROR: Failed to build APK
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! APK built successfully!
echo ========================================
echo.
echo APK location: bin\loadtester-1.0-arm64-v8a-debug.apk
echo.
echo To install on your phone:
echo 1. Enable USB Debugging on your phone
echo 2. Connect phone via USB
echo 3. Run: adb install bin\loadtester-1.0-arm64-v8a-debug.apk
echo.
pause
