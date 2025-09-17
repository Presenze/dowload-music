@echo off
echo 🚀 Installazione Railway CLI per Windows...

echo.
echo 📥 Scaricando Railway CLI...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/railwayapp/cli/releases/latest/download/railway-windows-x64.zip' -OutFile 'railway.zip'"

echo.
echo 📦 Estraendo Railway CLI...
powershell -Command "Expand-Archive -Path 'railway.zip' -DestinationPath '.' -Force"

echo.
echo 🔧 Installando Railway CLI...
move railway.exe %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\railway.exe

echo.
echo 🧹 Pulizia file temporanei...
del railway.zip

echo.
echo ✅ Railway CLI installato con successo!
echo.
echo 🔗 Aggiungi Railway al PATH:
echo setx PATH "%PATH%;%USERPROFILE%\AppData\Local\Microsoft\WindowsApps" /M
echo.
echo 🚀 Riavvia PowerShell e usa: railway --version
echo.
pause
