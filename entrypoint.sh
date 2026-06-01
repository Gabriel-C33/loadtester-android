#!/bin/bash
set -e

# Find and patch buildozer
find /home/user/.venv -name "__init__.py" -path "*/buildozer/*" -exec sed -i 's/cont = input/cont = "y" #input/g' {} \;

# Run buildozer
cd /app
buildozer -v android debug
