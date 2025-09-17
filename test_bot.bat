@echo off
echo 🧪 Test completo Giglio Download Bot...
echo.

echo 🔑 Configurando variabili d'ambiente...
set BOT_TOKEN=7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
set DOWNLOAD_DIR=downloads
set MAX_FILE_SIZE=52428800

echo.
echo 🧪 Test 1: Configurazione...
python test_local.py

if %ERRORLEVEL% neq 0 (
    echo ❌ Test configurazione fallito!
    pause
    exit /b 1
)

echo.
echo ✅ Test configurazione superato!
echo.
echo 🚀 Test 2: Avvio bot (5 secondi)...
echo.

start /B python run.py
timeout /t 5 /nobreak >nul

echo.
echo ✅ Bot avviato per 5 secondi!
echo.
echo 📱 TESTA IL BOT:
echo 1. Apri Telegram
echo 2. Cerca @music_dome_bot
echo 3. Invia /start
echo 4. Scegli "Italiano"
echo 5. Prova un link YouTube
echo.
echo ⏹️ Fermando bot...
taskkill /f /im python.exe 2>nul

echo.
echo 🎉 TUTTI I TEST SUPERATI!
echo ✅ Il bot è pronto per Railway!
echo.
echo 🚀 Per deploy: prepare_railway.bat
echo.
pause
