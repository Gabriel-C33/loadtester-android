#!/bin/bash

# This script installs Android SDK components needed for the build

export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# Wait for SDK to be downloaded by buildozer first
sleep 5

# Accept licenses
yes | sdkmanager --licenses 2>/dev/null || true

# Install required SDK components
sdkmanager "platform-tools" "platforms;android-33" "build-tools;30.0.3" 2>/dev/null || true

echo "SDK components installed"
