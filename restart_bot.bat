@echo off
echo 🔄 Riavvio Giglio Download Bot...
echo.
echo ⏹️  Terminando istanze esistenti...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo 🚀 Avviando bot...
python run.py
pause
