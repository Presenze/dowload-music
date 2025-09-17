#!/bin/bash
echo "🌸 Installazione pacchetti per Giglio Download Bot..."
echo

echo "📦 Aggiornando pip..."
python3 -m pip install --upgrade pip

echo
echo "📦 Installando pacchetti principali..."
pip3 install -r requirements.txt

echo
echo "🔧 Installando FFmpeg (opzionale ma raccomandato)..."
echo "Per Ubuntu/Debian: sudo apt install ffmpeg"
echo "Per macOS: brew install ffmpeg"
echo "Per CentOS/RHEL: sudo yum install ffmpeg"
echo

echo "✅ Installazione completata!"
echo
echo "🚀 Per avviare il bot: python3 run.py"
