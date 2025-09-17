@echo off
echo 🔧 Deploy Finale - Fix YouTube Completo...

echo.
echo 📦 Aggiungendo TUTTI i file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "FINAL FIX: YouTube authentication bypass + Railway optimization"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ DEPLOY COMPLETATO!
echo.
echo 🎯 Il bot ora dovrebbe funzionare perfettamente con YouTube!
echo.
echo Testa con:
echo - https://youtu.be/fJOE0vUjjo8?si=7P_VCMfO0wBwKq_Y
echo - https://www.youtube.com/watch?v=Q7NjUxGMv7Y&list=RDQ7NjUxGMv7Y&start_radio=1
echo.
echo Se non funziona, vai su Railway dashboard e fai redeploy manuale!
echo.
pause
