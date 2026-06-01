"""
Build APK using Chaquopy (Python for Android)
This creates a native Android app with Python support
"""

import os
import subprocess
import shutil

def create_android_project():
    """Create Android Studio project with Chaquopy"""
    
    project_name = "LoadTester"
    package_name = "org.loadtester.app"
    
    # Create project structure
    os.makedirs("android_project/app/src/main/python", exist_ok=True)
    os.makedirs("android_project/app/src/main/res/layout", exist_ok=True)
    os.makedirs("android_project/app/src/main/res/values", exist_ok=True)
    os.makedirs("android_project/app/src/main/java/org/loadtester/app", exist_ok=True)
    
    # Copy Python files
    shutil.copy("locustfile.py", "android_project/app/src/main/python/")
    
    # Create simplified main.py for Android
    with open("android_project/app/src/main/python/main.py", "w") as f:
        f.write("""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run locustfile
import locustfile

print("Load Tester Started!")
print("Check the app UI for controls")
""")
    
    # Create build.gradle (app level)
    with open("android_project/app/build.gradle", "w") as f:
        f.write("""
plugins {
    id 'com.android.application'
    id 'com.chaquo.python'
}

android {
    namespace 'org.loadtester.app'
    compileSdk 34
    
    defaultConfig {
        applicationId "org.loadtester.app"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
        
        ndk {
            abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
        }
        
        python {
            pip {
                install "requests"
                install "urllib3"
            }
        }
    }
    
    buildTypes {
        release {
            minifyEnabled false
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
}
""")
    
    # Create build.gradle (project level)
    with open("android_project/build.gradle", "w") as f:
        f.write("""
buildscript {
    repositories {
        google()
        mavenCentral()
        maven { url "https://chaquo.com/maven" }
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
        classpath 'com.chaquo.python:gradle:15.0.1'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
""")
    
    # Create MainActivity.java
    with open("android_project/app/src/main/java/org/loadtester/app/MainActivity.java", "w") as f:
        f.write("""
package org.loadtester.app;

import android.os.Bundle;
import android.widget.TextView;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        
        TextView output = findViewById(R.id.output);
        Button startBtn = findViewById(R.id.startBtn);
        EditText urlInput = findViewById(R.id.urlInput);
        
        startBtn.setOnClickListener(v -> {
            String url = urlInput.getText().toString();
            output.setText("Starting test for: " + url);
            
            // Run Python script
            Python py = Python.getInstance();
            py.getModule("main");
        });
    }
}
""")
    
    # Create layout
    with open("android_project/app/src/main/res/layout/activity_main.xml", "w") as f:
        f.write("""
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Load Tester"
        android:textSize="24sp"
        android:gravity="center"
        android:padding="16dp"/>
    
    <EditText
        android:id="@+id/urlInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Target URL"
        android:inputType="textUri"/>
    
    <Button
        android:id="@+id/startBtn"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="START TEST"/>
    
    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent">
        
        <TextView
            android:id="@+id/output"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Ready..."
            android:fontFamily="monospace"/>
    </ScrollView>
</LinearLayout>
""")
    
    # Create strings.xml
    with open("android_project/app/src/main/res/values/strings.xml", "w") as f:
        f.write("""
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Load Tester</string>
</resources>
""")
    
    # Create AndroidManifest.xml
    with open("android_project/app/src/main/AndroidManifest.xml", "w") as f:
        f.write("""
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.WAKE_LOCK"/>
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.Light">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
""")
    
    # Create settings.gradle
    with open("android_project/settings.gradle", "w") as f:
        f.write("""
include ':app'
rootProject.name = "LoadTester"
""")
    
    # Create gradle.properties
    with open("android_project/gradle.properties", "w") as f:
        f.write("""
android.useAndroidX=true
android.enableJetifier=true
""")
    
    print("✅ Android project created in 'android_project/' folder")
    print("\nNext steps:")
    print("1. Open 'android_project' in Android Studio")
    print("2. Wait for Gradle sync")
    print("3. Click 'Build' → 'Build Bundle(s) / APK(s)' → 'Build APK(s)'")
    print("4. APK will be in: android_project/app/build/outputs/apk/debug/")

if __name__ == "__main__":
    create_android_project()
