@echo off
echo 🌸 Installazione pacchetti per Giglio Download Bot...
echo.

echo 📦 Aggiornando pip...
python -m pip install --upgrade pip

echo.
echo 📦 Installando pacchetti principali...
pip install -r requirements.txt

echo.
echo 🔧 Installando FFmpeg (opzionale ma raccomandato)...
echo Per installare FFmpeg:
echo 1. Scarica da: https://ffmpeg.org/download.html
echo 2. Estrai in C:\ffmpeg
echo 3. Aggiungi C:\ffmpeg\bin al PATH di sistema
echo.

echo ✅ Installazione completata!
echo.
echo 🚀 Per avviare il bot: python run.py
pause
