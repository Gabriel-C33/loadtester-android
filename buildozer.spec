[app]
title = Load Tester
package.name = loadtester
package.domain = org.loadtester

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = python3,kivy,kivymd,requests,urllib3,pillow,android

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE

# Android services
services = LoadTesterService:service.py:foreground

# Android API level
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.sdk_path = 
android.ndk_path =

# Android background service
android.wakelock = True

# App icon (optional - create icon.png)
#icon.filename = %(source.dir)s/icon.png

# Presplash (optional - create presplash.png)
#presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
