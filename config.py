import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN') or 'TOKEN HERE'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit for Telegram
DOWNLOAD_DIR = "downloads"

# Supported platforms
SUPPORTED_PLATFORMS = {
    'youtube': ['youtube.com', 'youtu.be'],
    'instagram': ['instagram.com'],
    'tiktok': ['tiktok.com', 'vm.tiktok.com'],
    'twitter': ['twitter.com', 'x.com'],
    'facebook': ['facebook.com', 'fb.watch'],
    'reddit': ['reddit.com'],
    'vimeo': ['vimeo.com'],
    'dailymotion': ['dailymotion.com']
}

# File type configurations
FILE_TYPES = {
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.m4a'],
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar']
}

# Messages
MESSAGES = {
    'start': {
        'en': "🎵 Welcome to Giglio Download Unlimited! 🎵\n\nI can download music, videos, images, and files from various platforms:\n• YouTube\n• Instagram\n• TikTok\n• Twitter/X\n• Facebook\n• Reddit\n• And many more!\n\nJust send me a link or file!",
        'it': "🎵 Benvenuto in Giglio Download Unlimited! 🎵\n\nPosso scaricare musica, video, immagini e file da varie piattaforme:\n• YouTube\n• Instagram\n• TikTok\n• Twitter/X\n• Facebook\n• Reddit\n• E molte altre!\n\nMandami semplicemente un link o un file!"
    },
    'help': {
        'en': "📖 How to use:\n\n1. Send me a link from any supported platform\n2. I'll automatically detect the content type\n3. Choose your preferred quality/format\n4. Download and enjoy!\n\nSupported platforms: YouTube, Instagram, TikTok, Twitter, Facebook, Reddit, Vimeo, and more!",
        'it': "📖 Come usare:\n\n1. Mandami un link da qualsiasi piattaforma supportata\n2. Rileverò automaticamente il tipo di contenuto\n3. Scegli la qualità/formato preferito\n4. Scarica e goditi il contenuto!\n\nPiattaforme supportate: YouTube, Instagram, TikTok, Twitter, Facebook, Reddit, Vimeo e molte altre!"
    },
    'error': {
        'en': "❌ Sorry, I couldn't process that request. Please check the link and try again.",
        'it': "❌ Spiacente, non sono riuscito a processare quella richiesta. Controlla il link e riprova."
    },
    'youtube_error': {
        'en': "❌ This YouTube video requires sign-in or is restricted. Try a different video or use a regular YouTube link (not YouTube Music).",
        'it': "❌ Questo video YouTube richiede l'accesso o è limitato. Prova un video diverso o usa un link YouTube normale (non YouTube Music)."
    },
    'processing': {
        'en': "⏳ Processing your request...",
        'it': "⏳ Sto processando la tua richiesta..."
    },
    'downloading': {
        'en': "⏳ Downloading...",
        'it': "⏳ Scaricando..."
    },
    'download_complete': {
        'en': "✅ Download completed!",
        'it': "✅ Download completato!"
    },
    'file_saved': {
        'en': "✅ File saved successfully!",
        'it': "✅ File salvato con successo!"
    },
    'file_too_large': {
        'en': "❌ File too large. Maximum size:",
        'it': "❌ File troppo grande. Dimensione massima:"
    }
}
