#!/bin/bash

echo "========================================"
echo "Building Android APK using Docker"
echo "========================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed!"
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "Building Docker image..."
docker build -t loadtester-builder .

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build Docker image"
    exit 1
fi

echo
echo "Building APK (this may take 20-30 minutes on first run)..."
docker run --rm -v "$(pwd):/app" loadtester-builder

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build APK"
    exit 1
fi

echo
echo "========================================"
echo "SUCCESS! APK built successfully!"
echo "========================================"
echo
echo "APK location: bin/loadtester-1.0-arm64-v8a-debug.apk"
echo
echo "To install on your phone:"
echo "1. Enable USB Debugging on your phone"
echo "2. Connect phone via USB"
echo "3. Run: adb install bin/loadtester-1.0-arm64-v8a-debug.apk"
echo
