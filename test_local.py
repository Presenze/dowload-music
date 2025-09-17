#!/usr/bin/env python3
"""
Test script per verificare che il bot funzioni prima del deploy su Railway
"""

import os
import sys
from config import BOT_TOKEN, SUPPORTED_PLATFORMS

def test_configuration():
    """Testa la configurazione del bot"""
    print("🧪 Test configurazione Giglio Download Bot...")
    print("=" * 50)
    
    # Test token
    if BOT_TOKEN:
        print("✅ BOT_TOKEN configurato")
        print(f"   Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
    else:
        print("❌ BOT_TOKEN non trovato!")
        print("   Configura la variabile d'ambiente BOT_TOKEN")
        return False
    
    # Test piattaforme supportate
    print(f"✅ Piattaforme supportate: {len(SUPPORTED_PLATFORMS)}")
    for platform, domains in SUPPORTED_PLATFORMS.items():
        print(f"   - {platform}: {', '.join(domains)}")
    
    # Test dipendenze
    print("\n📦 Test dipendenze...")
    try:
        import telegram
        print("✅ python-telegram-bot installato")
    except ImportError:
        print("❌ python-telegram-bot non installato")
        return False
    
    try:
        import yt_dlp
        print("✅ yt-dlp installato")
    except ImportError:
        print("❌ yt-dlp non installato")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp installato")
    except ImportError:
        print("❌ aiohttp non installato")
        return False
    
    # Test directory
    print("\n📁 Test directory...")
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        print("✅ Directory downloads creata")
    else:
        print("✅ Directory downloads esiste")
    
    print("\n🎉 Tutti i test superati!")
    print("✅ Il bot è pronto per il deploy su Railway!")
    return True

def test_bot_connection():
    """Testa la connessione al bot"""
    print("\n🔗 Test connessione bot...")
    try:
        from telegram import Bot
        bot = Bot(token=BOT_TOKEN)
        
        # Test connessione
        import asyncio
        async def test_connection():
            try:
                me = await bot.get_me()
                print(f"✅ Bot connesso: @{me.username}")
                return True
            except Exception as e:
                print(f"❌ Errore connessione: {e}")
                return False
        
        return asyncio.run(test_connection())
    except Exception as e:
        print(f"❌ Errore creazione bot: {e}")
        return False

if __name__ == "__main__":
    print("🌸 Giglio Download Bot - Test Pre-Deploy")
    print("=" * 50)
    
    # Test configurazione
    if not test_configuration():
        print("\n❌ Test configurazione fallito!")
        sys.exit(1)
    
    # Test connessione bot
    if not test_bot_connection():
        print("\n❌ Test connessione fallito!")
        sys.exit(1)
    
    print("\n🚀 TUTTI I TEST SUPERATI!")
    print("✅ Il bot è pronto per Railway!")
    print("\n📋 Prossimi passi:")
    print("1. Esegui: setup_git.bat")
    print("2. Crea repository su GitHub")
    print("3. Deploy su Railway")
    print("4. Configura variabili d'ambiente")
    print("5. Avvia il bot!")
