# Build Android APK - Load Tester

## Quick Start (Recommended)

### Option 1: GitHub Actions (Easiest)
1. Push code to GitHub
2. GitHub Actions automatically builds the APK
3. Download from Releases page: https://github.com/Gabriel-C33/loadtester-android/releases

### Option 2: Docker Build (Windows/Mac/Linux)
```powershell
# Windows PowerShell
.\build_docker.ps1

# Linux/Mac
chmod +x build_apk.sh
./build_apk.sh
```

The APK will be in `bin/` directory.

## What Was Fixed

### Previous Issues:
1. **App crashed on launch** - KivyMD compatibility issues
2. **GitHub Actions build failed** - libffi compilation errors
3. **Docker root permission errors** - Buildozer running as root

### Solutions Applied:
1. **Removed KivyMD** - Now using pure Kivy (more stable)
2. **Fixed dependencies** - Pinned Python 3.11.6 and Kivy 2.3.0
3. **Updated build tools** - Added missing autotools (m4, gettext, texinfo)
4. **Fixed Docker** - Now runs as non-root user
5. **Simplified UI** - Removed complex features causing crashes

## Current Features

The APK now includes:
- ✅ Simple, stable UI (pure Kivy)
- ✅ Configurable URL, requests, threads
- ✅ Background threading for tests
- ✅ Real-time progress updates
- ✅ Save/load configuration
- ✅ Basic load testing with requests library

## Next Steps: Add Full Locust Features

To integrate your original `locustfile.py` with all advanced features:

### 1. Create a wrapper module
```python
# loadtester/engine.py
from locustfile import *

def run_advanced_test(url, requests, threads, **kwargs):
    # Your full locust logic here
    pass
```

### 2. Update main.py to use it
```python
from loadtester.engine import run_advanced_test

def run_test(self, url, requests_count, threads_count):
    run_advanced_test(url, requests_count, threads_count)
```

### 3. Update buildozer.spec
Add to requirements:
```
requirements = python3==3.11.6,kivy==2.3.0,requests,urllib3,certifi,charset-normalizer,idna,android,gevent,locust
```

## Build Requirements

### Docker Method:
- Docker Desktop installed and running
- 4GB+ free disk space
- 30-60 minutes build time

### GitHub Actions:
- GitHub account
- Repository with code
- Automatic builds on push

## Troubleshooting

### APK crashes on launch:
- Check Android version (requires Android 5.0+)
- Check logcat: `adb logcat | grep python`
- Try simplified version first

### Build fails:
- Clean build: `rm -rf .buildozer bin`
- Update Docker: `docker pull ubuntu:22.04`
- Check disk space: Need 4GB+ free

### GitHub Actions fails:
- Check Actions tab for detailed logs
- Common issues: timeout, dependency conflicts
- Wait for retry (automatic on push)

## File Structure

```
loadtester-android/
├── main.py              # Kivy UI (simplified, stable)
├── locustfile.py        # Your original load testing script
├── buildozer.spec       # Build configuration
├── Dockerfile           # Docker build environment
├── entrypoint.sh        # Docker entrypoint
├── build_docker.ps1     # Windows build script
├── build_apk.sh         # Linux/Mac build script
└── .github/
    └── workflows/
        └── build-apk.yml # GitHub Actions workflow
```

## Testing the APK

1. Install on Android device:
   ```bash
   adb install bin/loadtester-*.apk
   ```

2. Grant permissions:
   - Internet access (automatic)
   - Storage access (if needed)

3. Run test:
   - Enter URL (e.g., https://example.com)
   - Set requests (e.g., 100)
   - Set threads (e.g., 10)
   - Tap "START TEST"

## Known Limitations

Current version:
- Basic load testing only (not full locust features yet)
- No WAF bypass techniques (from original script)
- No user agent rotation
- No IP spoofing
- No advanced statistics

To add these features, we need to integrate the full `locustfile.py` logic.

## Support

- GitHub Issues: https://github.com/Gabriel-C33/loadtester-android/issues
- Check Actions logs for build errors
- Use `adb logcat` for runtime errors
