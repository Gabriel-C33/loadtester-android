# How to Build the Android APK

You have **3 options** to build the APK:

---

## Option 1: Docker (Recommended for Windows)

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Steps

**On Windows:**
```bash
build_apk.bat
```

**On Linux/Mac:**
```bash
chmod +x build_apk.sh
./build_apk.sh
```

This will:
1. Build a Docker container with all dependencies
2. Compile the APK inside the container
3. Output: `bin/loadtester-1.0-arm64-v8a-debug.apk`

**First build takes 20-30 minutes** (downloads Android SDK, NDK, etc.)
Subsequent builds are much faster (~5 minutes)

---

## Option 2: WSL (Windows Subsystem for Linux)

### Prerequisites
1. Enable WSL2:
   ```powershell
   wsl --install
   ```

2. Install Ubuntu from Microsoft Store

3. Open Ubuntu terminal

### Steps in WSL Ubuntu:

```bash
# Install dependencies
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install buildozer
pip3 install buildozer cython

# Navigate to your project (adjust path)
cd /mnt/c/Users/YourUsername/path/to/project

# Build APK
buildozer -v android debug
```

Output: `bin/loadtester-1.0-arm64-v8a-debug.apk`

---

## Option 3: Linux (Native)

### Prerequisites
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### Steps
```bash
# Install buildozer
pip3 install buildozer cython

# Build APK
buildozer -v android debug
```

Output: `bin/loadtester-1.0-arm64-v8a-debug.apk`

---

## Option 4: Quick Test with Kivy Launcher (No Build Required!)

### For Quick Testing Only

1. Install [Kivy Launcher](https://play.google.com/store/apps/details?id=org.kivy.pygame) from Google Play Store

2. Create folder on phone: `/sdcard/kivy/loadtester/`

3. Copy these files to that folder:
   - `main.py`
   - `locustfile.py`
   - `service.py`

4. Open Kivy Launcher and select "loadtester"

**Note:** This won't have background service support, but good for testing the UI.

---

## Installing the APK on Your Phone

### Method 1: USB Cable
```bash
# Enable USB Debugging on phone first
adb install bin/loadtester-1.0-arm64-v8a-debug.apk
```

### Method 2: Manual Install
1. Copy APK to phone
2. Open file manager on phone
3. Tap the APK file
4. Allow "Install from Unknown Sources" if prompted
5. Install

---

## Troubleshooting

### Docker build fails
- Ensure Docker Desktop is running
- Check you have at least 10GB free disk space
- Try: `docker system prune -a` to clean up

### WSL build fails
- Update WSL: `wsl --update`
- Ensure you have enough disk space in WSL
- Try: `buildozer android clean` then rebuild

### "buildozer: command not found"
```bash
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin
```

### Build succeeds but APK crashes
- Check Android version (minimum 5.0 / API 21)
- Check logs: `adb logcat | grep python`
- Try: `buildozer android clean` then rebuild

### Background service doesn't work
- Disable battery optimization for the app
- Settings → Apps → Load Tester → Battery → Unrestricted

---

## Build Time Expectations

| Build Type | First Build | Subsequent Builds |
|------------|-------------|-------------------|
| Docker     | 20-30 min   | 5-10 min         |
| WSL        | 20-30 min   | 5-10 min         |
| Linux      | 20-30 min   | 5-10 min         |

First build downloads:
- Android SDK (~1GB)
- Android NDK (~1GB)
- Python dependencies
- Compiles everything

---

## What You Get

✅ Fully functional Android APK
✅ Runs your exact locustfile.py script
✅ Background service support
✅ Data persistence
✅ All WAF bypass features
✅ 50K+ user agents
✅ Works offline (after first run)

---

## Need Help?

Common issues:
- **Out of memory**: Close other apps, increase Docker memory limit
- **Slow build**: Normal for first build, be patient
- **Permission denied**: Run with sudo (Linux) or as Administrator (Windows)
