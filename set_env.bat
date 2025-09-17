@echo off
echo 🌸 Configurazione variabili d'ambiente per Giglio Download Bot...
echo.

echo 🔑 Impostando BOT_TOKEN...
set BOT_TOKEN=7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8

echo 📁 Impostando DOWNLOAD_DIR...
set DOWNLOAD_DIR=downloads

echo 📊 Impostando MAX_FILE_SIZE...
set MAX_FILE_SIZE=52428800

echo.
echo ✅ Variabili d'ambiente configurate!
echo.
echo 🧪 Testando configurazione...
python test_local.py

echo.
echo 🚀 Se il test è OK, puoi procedere con:
echo 1. setup_git.bat
echo 2. Deploy su Railway
echo.
pause
