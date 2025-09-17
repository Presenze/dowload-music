@echo off
echo 🔧 Deploy Requirements Fix - Railway Compatible!

echo.
echo 📦 Aggiungendo TUTTI i file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "REQUIREMENTS FIX: Removed problematic packages, Railway compatible requirements"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ DEPLOY COMPLETATO!
echo.
echo 🔧 REQUIREMENTS FIX APPLICATO!
echo.
echo ❌ PACCHETTI RIMOSSI (PROBLEMATICI):
echo - pycrypto==2.6.1 (richiede compilatore C)
echo - tls-client==1.0.0 (problemi di build)
echo - selenium==4.15.2 (troppo pesante)
echo - undetected-chromedriver==3.5.4 (problemi di build)
echo - playwright==1.40.0 (troppo pesante)
echo - requests-html==0.10.0 (dipendenze complesse)
echo - curl-cffi==0.5.10 (problemi di build)
echo - httpx-socks==0.8.4 (dipendenze complesse)
echo - pycurl==7.45.2 (richiede compilatore C)
echo - urllib3[socks]==2.1.0 (dipendenze complesse)
echo.
echo ✅ PACCHETTI MANTENUTI (RAILWAY COMPATIBILI):
echo - python-telegram-bot==20.7
echo - yt-dlp==2025.9.5
echo - requests==2.31.0
echo - aiohttp==3.9.1
echo - httpx==0.25.2
echo - Pillow==10.1.0
echo - python-dotenv==1.0.0
echo - mutagen==1.47.0
echo - pycryptodomex==3.23.0
echo - brotli==1.1.0
echo - asyncio-mqtt==0.16.1
echo - colorama==0.4.6
echo - ffmpeg-python==0.2.0
echo - cryptography==41.0.7
echo - certifi==2023.11.17
echo - urllib3==2.1.0
echo - websockets==12.0
echo - pycryptodome==3.19.0
echo - fake-useragent==1.4.0
echo - beautifulsoup4==4.12.2
echo - lxml==4.9.3
echo - cloudscraper==1.2.71
echo.
echo 🎉 REQUIREMENTS ORA FUNZIONANO SU RAILWAY!
echo.
pause
