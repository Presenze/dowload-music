@echo off
echo 🔄 Force Rebuild - Forza Nuovo Deploy!

echo.
echo 📦 Aggiungendo TUTTI i file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "FORCE REBUILD: Added VERSION.txt to force Railway rebuild with clean requirements"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ FORCE REBUILD COMPLETATO!
echo.
echo 🔄 Railway ora dovrebbe fare un rebuild completo!
echo.
echo 📋 VERSIONE: v2.0.0 - Clean Requirements Fix
echo.
echo 🎯 REQUIREMENTS PULITI:
echo - Solo pacchetti Railway compatibili
echo - Nessun pacchetto che richiede compilatore C
echo - YouTube Revolution Bypass attivo
echo.
echo 🎉 IL BOT DOVREBBE FUNZIONARE PERFETTAMENTE!
echo.
pause
