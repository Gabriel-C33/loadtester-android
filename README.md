# Load Tester - Mobile Android App

Mobile load testing application that runs your exact locustfile.py script on Android devices.

## Features

✅ Runs original locustfile.py 1:1  
✅ All inputs configurable from UI  
✅ Works in background  
✅ Saves all data  
✅ Test websites worldwide from your phone  

## Download APK

Go to [Releases](../../releases) and download the latest APK.

Or check [Actions](../../actions) for the latest build.

## Install

1. Download the APK
2. Enable "Install from Unknown Sources" on your phone
3. Install the APK
4. Open the app
5. Configure and start testing!

## Configuration

- **Target URL**: Website to test
- **Number of Requests**: Total requests to send
- **Concurrent Threads**: Parallel connections
- **Timeout**: Request timeout in seconds
- **Infinity Mode**: Loop forever
- **Cycle Delay**: Delay between cycles

## Permissions

- **INTERNET**: Make HTTP requests
- **WAKE_LOCK**: Keep device awake
- **FOREGROUND_SERVICE**: Run in background
- **ACCESS_NETWORK_STATE**: Check connectivity

## Build from Source

```bash
# Install buildozer
pip install buildozer

# Build APK
buildozer android debug
```

APK will be in `bin/` folder.

## License

MIT
