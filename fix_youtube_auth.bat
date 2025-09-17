@echo off
echo 🔧 Fix YouTube Authentication su Railway...

echo.
echo 📦 Aggiungendo file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "Fix YouTube authentication bypass - Add mobile client and fallback"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ Fix completato!
echo.
echo 🎯 Il bot ora bypassa l'autenticazione YouTube!
echo.
echo Testa con:
echo - https://youtu.be/fJOE0vUjjo8?si=7P_VCMfO0wBwKq_Y
echo - https://www.youtube.com/watch?v=Q7NjUxGMv7Y&list=RDQ7NjUxGMv7Y&start_radio=1
echo.
pause
