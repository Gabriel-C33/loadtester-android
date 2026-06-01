#!/bin/bash
set -e

echo "Starting APK build..."

# Run buildozer
cd /app
buildozer -v android debug

echo "Build completed!"
