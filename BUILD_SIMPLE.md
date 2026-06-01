# Най-лесен начин да build-неш APK

## Използвай онлайн сървиз (ПРЕПОРЪЧВАМ!)

### GitHub Actions (Безплатно)

1. Качи проекта в GitHub
2. Създай `.github/workflows/build.yml`:

```yaml
name: Build APK

on: [push, workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          workdir: .
          buildozer_version: stable
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: loadtester-apk
          path: bin/*.apk
```

3. Push кода
4. GitHub автоматично ще build-не APK-то
5. Свали от "Actions" → "Artifacts"

---

## Или използвай готов APK builder онлайн

### Replit (Най-лесно!)

1. Отиди на https://replit.com
2. Създай нов Python Repl
3. Upload файловете
4. Инсталирай buildozer:
   ```bash
   pip install buildozer
   ```
5. Run:
   ```bash
   buildozer android debug
   ```

---

## Локално на Windows (WSL)

```powershell
# Инсталирай WSL
wsl --install

# Отвори Ubuntu
wsl

# В Ubuntu:
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

pip3 install buildozer

# Navigate to project
cd /mnt/c/Users/YourName/Desktop/loadtest

# Build
buildozer android debug
```

APK ще е в `bin/` папката!

---

## Защо Docker не работи?

Docker image-ът на Kivy има проблем с root permissions който не може да се заобиколи лесно. WSL или GitHub Actions са по-добри опции.
