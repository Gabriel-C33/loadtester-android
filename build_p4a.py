"""
Build APK using python-for-android directly
This is the most reliable method that works on Windows
"""

import subprocess
import os

def build_apk():
    """Build APK using p4a"""
    
    print("🚀 Building APK with python-for-android...")
    print("This will take 15-20 minutes on first run\n")
    
    # Create recipe for our app
    recipe = """
from pythonforandroid.recipe import PythonRecipe

class LoadTesterRecipe(PythonRecipe):
    version = '1.0'
    url = 'file://.'
    depends = ['python3', 'requests', 'urllib3']
    site_packages_name = 'loadtester'
    call_hostpython_via_targetpython = False

recipe = LoadTesterRecipe()
"""
    
    os.makedirs("p4a_recipes/loadtester", exist_ok=True)
    with open("p4a_recipes/loadtester/__init__.py", "w") as f:
        f.write(recipe)
    
    # Build command
    cmd = [
        "p4a",
        "apk",
        "--private", ".",
        "--package", "org.loadtester.app",
        "--name", "LoadTester",
        "--version", "1.0",
        "--bootstrap", "sdl2",
        "--requirements", "python3,kivy,requests,urllib3",
        "--permission", "INTERNET",
        "--permission", "WAKE_LOCK",
        "--orientation", "portrait",
        "--arch", "armeabi-v7a",
        "--arch", "arm64-v8a",
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("\n✅ APK built successfully!")
        print("📦 APK location: Check the output above for the path")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed:")
        print(e.stdout)
        print(e.stderr)
        print("\n💡 Try using WSL or Docker instead")

if __name__ == "__main__":
    build_apk()
