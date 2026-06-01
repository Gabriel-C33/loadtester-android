
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run locustfile
import locustfile

print("Load Tester Started!")
print("Check the app UI for controls")
