@echo off
echo 🚀 Preparazione per deploy su Railway...
echo.

echo 🔑 Configurando variabili d'ambiente...
set BOT_TOKEN=7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
set DOWNLOAD_DIR=downloads
set MAX_FILE_SIZE=52428800

echo.
echo 🧪 Testando configurazione...
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
echo 💾 Commit iniziale...
git commit -m "Giglio Download Bot - Ready for Railway Deploy"

echo.
echo ✅ Repository Git preparato!
echo.
echo 📋 PROSSIMI PASSI:
echo.
echo 1️⃣ Crea repository su GitHub:
echo    - Vai su https://github.com/new
echo    - Nome: giglio-download-bot
echo    - Clicca "Create repository"
echo.
echo 2️⃣ Collega repository locale:
echo    git remote add origin https://github.com/TUO_USERNAME/giglio-download-bot.git
echo    git push -u origin main
echo.
echo 3️⃣ Deploy su Railway:
echo    - Vai su https://railway.app
echo    - Login con GitHub
echo    - "New Project" → "Deploy from GitHub repo"
echo    - Seleziona giglio-download-bot
echo.
echo 4️⃣ Configura variabili d'ambiente su Railway:
echo    BOT_TOKEN = 7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
echo    DOWNLOAD_DIR = downloads
echo    MAX_FILE_SIZE = 52428800
echo.
echo 5️⃣ Il bot sarà online 24/7!
echo.
echo 🎉 TUTTO PRONTO PER RAILWAY!
echo.
pause
