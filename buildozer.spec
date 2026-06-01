[app]
title = Load Tester
package.name = loadtester
package.domain = org.loadtester

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = python3==3.11.6,kivy==2.3.0,requests,urllib3,certifi,charset-normalizer,idna,android

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE

# Android services (disabled for now to fix crashes)
# services = LoadTesterService:service.py:foreground

# Android API level
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.sdk_path = 
android.ndk_path =
android.gradle_dependencies = 

# Android background service
android.wakelock = True

# App icon (optional - create icon.png)
#icon.filename = %(source.dir)s/icon.png

# Presplash (optional - create presplash.png)
#presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
