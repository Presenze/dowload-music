@echo off
echo 🔧 Fix e Deploy Bot su Railway...

echo.
echo 📦 Aggiungendo file al Git...
git add .

echo.
echo 💾 Commit delle modifiche...
git commit -m "Fix YouTube downloads and add generic URL support"

echo.
echo 🚀 Push su GitHub...
git push origin main

echo.
echo 🔄 Deploy su Railway...
cmd /c "railway up"

echo.
echo ✅ Deploy completato!
echo.
echo 🤖 Il bot dovrebbe essere online su Railway!
echo.
pause
