@echo off
echo 🔧 Deploy Minimal - Requirements Super Minimale!

echo.
echo 📦 Aggiungendo TUTTI i file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "MINIMAL: Super minimal requirements.txt with only essential packages"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ DEPLOY MINIMALE COMPLETATO!
echo.
echo 🔧 REQUIREMENTS SUPER MINIMALI:
echo - python-telegram-bot==20.7
echo - yt-dlp==2025.9.5
echo - requests==2.31.0
echo - aiohttp==3.9.1
echo - python-dotenv==1.0.0
echo - mutagen==1.47.0
echo - colorama==0.4.6
echo - cryptography==41.0.7
echo - certifi==2023.11.17
echo - urllib3==2.1.0
echo - fake-useragent==1.4.0
echo.
echo ❌ RIMOSSI TUTTI I PACCHETTI PROBLEMATICI:
echo - pycryptodomex (potrebbe causare conflitti)
echo - brotli (compressione non essenziale)
echo - asyncio-mqtt (non necessario)
echo - ffmpeg-python (problemi di build)
echo - websockets (dipendenze complesse)
echo - pycryptodome (conflitto con cryptography)
echo - beautifulsoup4 (parsing non essenziale)
echo - lxml (dipendenze complesse)
echo - cloudscraper (bypass non essenziale)
echo - httpx (ridondante con requests)
echo - Pillow (image processing non essenziale)
echo.
echo 🎉 SOLO PACCHETTI ESSENZIALI!
echo.
pause
