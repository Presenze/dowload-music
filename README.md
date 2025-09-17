# 🌸 Giglio Download Unlimited Bot

A powerful Telegram bot for downloading music, videos, images, and files from various social media platforms and websites.

## 🌍 Languages / Lingue

- **English** (below)
- **Italiano** (sotto)

---

## 🇬🇧 English

### Features

- 🎵 **Music Downloads**: Download audio from YouTube, SoundCloud, and more
- 📹 **Video Downloads**: Get videos from YouTube, Instagram, TikTok, Vimeo
- 📷 **Image Downloads**: Download images from Instagram, Twitter, Reddit
- 📄 **File Downloads**: Support for various file types and documents
- 🌐 **Multi-Platform**: Works with 20+ popular platforms
- 🔄 **Quality Selection**: Choose your preferred quality/format
- 🌍 **Multi-Language**: English and Italian support
- 📱 **User-Friendly**: Simple interface with inline keyboards

### Supported Platforms

- YouTube (youtube.com, youtu.be)
- Instagram (instagram.com)
- TikTok (tiktok.com, vm.tiktok.com)
- Twitter/X (twitter.com, x.com)
- Facebook (facebook.com, fb.watch)
- Reddit (reddit.com)
- Vimeo (vimeo.com)
- Dailymotion (dailymotion.com)
- And many more!

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd giglio-download-bot
   ```

2. **Install dependencies**
   ```bash
   # Windows: Run install_requirements.bat
   # Linux/Mac: Run ./install_requirements.sh
   # Manual: pip install -r requirements.txt
   ```

3. **Install FFmpeg** (recommended for best quality)
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`

4. **Get a Telegram Bot Token**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the token to `config.py`

5. **Run the bot**
   ```bash
   # Windows: start_bot.bat or python run.py
   # Linux/Mac: python3 run.py
   ```

### Usage

1. Start a conversation with your bot
2. Choose your language (English/Italiano)
3. Send a link from any supported platform
4. Select your preferred quality/format
5. Download and enjoy!

### Commands

- `/start` - Start the bot and choose language
- `/help` - Show help information

### Configuration

Edit `config.py` to customize:
- Supported platforms
- File type configurations
- Messages and translations
- File size limits

### Requirements

- Python 3.8+
- Telegram Bot Token
- Internet connection

---

## 🇮🇹 Italiano

### Caratteristiche

- 🎵 **Download Musica**: Scarica audio da YouTube, SoundCloud e altri
- 📹 **Download Video**: Ottieni video da YouTube, Instagram, TikTok, Vimeo
- 📷 **Download Immagini**: Scarica immagini da Instagram, Twitter, Reddit
- 📄 **Download File**: Supporto per vari tipi di file e documenti
- 🌐 **Multi-Piattaforma**: Funziona con 20+ piattaforme popolari
- 🔄 **Selezione Qualità**: Scegli la qualità/formato preferito
- 🌍 **Multi-Lingua**: Supporto inglese e italiano
- 📱 **User-Friendly**: Interfaccia semplice con tastiere inline

### Piattaforme Supportate

- YouTube (youtube.com, youtu.be)
- Instagram (instagram.com)
- TikTok (tiktok.com, vm.tiktok.com)
- Twitter/X (twitter.com, x.com)
- Facebook (facebook.com, fb.watch)
- Reddit (reddit.com)
- Vimeo (vimeo.com)
- Dailymotion (dailymotion.com)
- E molte altre!

### Installazione

1. **Clona il repository**
   ```bash
   git clone <repository-url>
   cd giglio-download-bot
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura le variabili d'ambiente**
   ```bash
   cp env_example.txt .env
   # Modifica .env e aggiungi il tuo bot token
   ```

4. **Ottieni un Token Bot Telegram**
   - Messaggia [@BotFather](https://t.me/botfather) su Telegram
   - Crea un nuovo bot con `/newbot`
   - Copia il token nel tuo file `.env`

5. **Avvia il bot**
   ```bash
   python bot.py
   ```

### Utilizzo

1. Inizia una conversazione con il tuo bot
2. Scegli la tua lingua (English/Italiano)
3. Invia un link da qualsiasi piattaforma supportata
4. Seleziona la qualità/formato preferito
5. Scarica e goditi il contenuto!

### Comandi

- `/start` - Avvia il bot e scegli la lingua
- `/help` - Mostra informazioni di aiuto

### Configurazione

Modifica `config.py` per personalizzare:
- Piattaforme supportate
- Configurazioni tipi di file
- Messaggi e traduzioni
- Limiti dimensione file

### Requisiti

- Python 3.8+
- Token Bot Telegram
- Connessione internet

---

## 📁 Project Structure

```
giglio-download-bot/
├── bot.py              # Main bot file
├── downloader.py       # Download manager
├── utils.py           # Utility functions
├── config.py          # Configuration
├── requirements.txt   # Python dependencies
├── env_example.txt    # Environment variables example
├── README.md          # This file
└── downloads/         # Download directory (created automatically)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This bot is for educational purposes only. Please respect copyright laws and terms of service of the platforms you download from.

---

**Made with ❤️ by the Giglio Download Unlimited Team**
