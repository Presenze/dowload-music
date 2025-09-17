@echo off
echo 🛑 Fermando tutte le istanze del bot...

echo.
echo 🔍 Cercando processi Python...
tasklist | findstr python

echo.
echo ⚡ Terminando tutti i processi Python...
taskkill /f /im python.exe 2>nul
taskkill /f /im python3.exe 2>nul

echo.
echo ✅ Tutte le istanze del bot sono state fermate!
echo.
echo 🚀 Ora il bot su Railway dovrebbe funzionare senza conflitti!
echo.
pause
