# Load Tester Android App

## Features
- ✅ Runs your original locustfile.py script 1:1
- ✅ All inputs configurable from UI (no hardcoded values)
- ✅ Works in background even when app is minimized
- ✅ Saves all data and configuration
- ✅ Foreground service keeps it running
- ✅ Test websites worldwide from your phone

## Building the APK

### Prerequisites
1. Install Python 3.8+
2. Install buildozer:
   ```bash
   pip install buildozer
   ```

3. Install Android SDK dependencies (Linux/WSL):
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

### Build APK

1. Navigate to project directory:
   ```bash
   cd /path/to/your/project
   ```

2. Initialize buildozer (first time only):
   ```bash
   buildozer init
   ```

3. Build the APK:
   ```bash
   buildozer -v android debug
   ```

4. The APK will be in `bin/` folder:
   ```
   bin/loadtester-1.0-arm64-v8a-debug.apk
   ```

### Install on Phone

1. Enable "Developer Options" and "USB Debugging" on your Android phone

2. Connect phone via USB

3. Install directly:
   ```bash
   buildozer android deploy run
   ```

   OR manually:
   ```bash
   adb install bin/loadtester-1.0-arm64-v8a-debug.apk
   ```

## Using the App

1. **Launch the app**

2. **Configure test parameters:**
   - Target URL (e.g., https://example.com)
   - Number of Requests (e.g., 10000)
   - Concurrent Threads (e.g., 100)
   - Timeout (seconds) (e.g., 15)
   - Infinity Mode (toggle on/off)
   - Cycle Delay (seconds) (e.g., 8)

3. **Press START TEST**

4. **Monitor output** - Real-time statistics will appear

5. **Background operation:**
   - Press home button - app continues running
   - You'll see a notification "Load Tester - Running in background"
   - Test continues even with screen off

6. **Data persistence:**
   - Configuration is auto-saved
   - Test output saved to `test_output.txt`
   - Reopen app to see previous results

## Permissions

The app requires:
- **INTERNET** - To make HTTP requests
- **WAKE_LOCK** - To keep CPU awake during tests
- **FOREGROUND_SERVICE** - To run in background
- **STORAGE** - To save test results

## Troubleshooting

### Build fails
- Make sure you have enough disk space (5GB+)
- Check Java version: `java -version` (should be 11 or 17)
- Clean build: `buildozer android clean`

### App crashes on start
- Check Android version (minimum Android 5.0 / API 21)
- Check logcat: `adb logcat | grep python`

### Background service stops
- Disable battery optimization for the app
- Settings → Apps → Load Tester → Battery → Unrestricted

## Files

- `main.py` - Main app UI
- `locustfile.py` - Your original load testing script
- `service.py` - Background service
- `buildozer.spec` - Build configuration
- `config.json` - Saved configuration (auto-generated)
- `test_output.txt` - Test output (auto-generated)

## Notes

- The app runs your EXACT original script
- All WAF bypass techniques included
- 50K+ user agents generated
- IP rotation and advanced headers
- Full statistics and reporting
- Works on any Android 5.0+ device
