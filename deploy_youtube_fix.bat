@echo off
echo 🔧 Deploy YouTube Fix Finale...

echo.
echo 📦 Aggiungendo TUTTI i file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "FINAL YOUTUBE FIX: Alternative downloader with music client bypass"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ DEPLOY COMPLETATO!
echo.
echo 🎯 Il bot ora usa un metodo alternativo per YouTube!
echo.
echo Testa con:
echo - https://youtu.be/fJOE0vUjjo8?si=7P_VCMfO0wBwKq_Y
echo - https://www.youtube.com/watch?v=Q7NjUxGMv7Y&list=RDQ7NjUxGMv7Y&start_radio=1
echo.
echo Se non funziona, il bot mostrerà opzioni di fallback!
echo.
pause
