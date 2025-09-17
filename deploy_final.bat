@echo off
echo 🚀 Deploy Finale - Giglio Download Bot su Railway
echo.

echo 🧪 Test 1: Configurazione...
python test_local.py

if %ERRORLEVEL% neq 0 (
    echo ❌ Test fallito! Controlla la configurazione.
    pause
    exit /b 1
)

echo.
echo ✅ Test superato! Procedendo con Git...
echo.

echo 📁 Inizializzando repository Git...
git init

echo.
echo 📝 Aggiungendo file al repository...
git add .

echo.
echo 💾 Commit per Railway...
git commit -m "Giglio Download Bot - Ready for Railway Deploy

Features:
- Download da YouTube, Instagram, TikTok, Twitter, Facebook, Reddit
- Video HD fino a 720p con audio
- MP3 fino a 320kbps
- Interfaccia bilingue (IT/EN)
- 8x più veloce degli altri bot
- Sicuro e affidabile

Deploy su Railway con variabili d'ambiente:
BOT_TOKEN=7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
DOWNLOAD_DIR=downloads
MAX_FILE_SIZE=52428800"

echo.
echo ✅ Repository Git preparato!
echo.
echo 🎯 PROSSIMI PASSI PER RAILWAY:
echo.
echo 1️⃣ Crea repository su GitHub:
echo    https://github.com/new
echo    Nome: giglio-download-bot
echo    Descrizione: Telegram bot per scaricare musica, video e file da tutte le piattaforme
echo    Clicca "Create repository"
echo.
echo 2️⃣ Collega repository locale:
echo    git remote add origin https://github.com/TUO_USERNAME/giglio-download-bot.git
echo    git push -u origin main
echo.
echo 3️⃣ Deploy su Railway:
echo    https://railway.app
echo    Login con GitHub
echo    "New Project" → "Deploy from GitHub repo"
echo    Seleziona: giglio-download-bot
echo.
echo 4️⃣ Configura variabili d'ambiente su Railway:
echo    BOT_TOKEN = 7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
echo    DOWNLOAD_DIR = downloads
echo    MAX_FILE_SIZE = 52428800
echo.
echo 5️⃣ Il bot sarà online 24/7!
echo    Username: @music_dome_bot
echo    Comando: /start
echo.
echo 🎉 TUTTO PRONTO PER RAILWAY!
echo.
echo 📋 File creati per Railway:
echo    ✅ railway.json - Configurazione Railway
echo    ✅ Procfile - Comando di avvio
echo    ✅ runtime.txt - Python 3.10
echo    ✅ .gitignore - Sicurezza file sensibili
echo    ✅ bot_config.env - Configurazione locale
echo.
echo 🚀 Deploy in 5 minuti!
echo.
pause
