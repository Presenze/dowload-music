#!/usr/bin/env python3
"""
Professional Bot - Il migliore downloader in circolazione
Bot Telegram professionale con interfaccia avanzata e funzionalità complete
"""

import os
import re
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from professional_downloader import ProfessionalDownloader
from config import BOT_TOKEN, MESSAGES, MAX_FILE_SIZE
from utils import format_file_size, sanitize_filename

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ProfessionalBot:
    def __init__(self):
        self.downloader = ProfessionalDownloader()
        self.user_sessions = {}  # Store user sessions
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start con interfaccia professionale"""
        user_id = update.effective_user.id
        
        # Inizializza sessione utente
        self.user_sessions[user_id] = {
            'language': 'it',
            'downloads': [],
            'preferences': {}
        }
        
        keyboard = [
            [InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = """
🎵 **GIGLIO DOWNLOAD UNLIMITED** 🎵
*Il migliore downloader in circolazione!*

🌍 **Scegli la tua lingua / Choose your language:**
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help con guide complete"""
        user_id = update.effective_user.id
        lang = self.user_sessions.get(user_id, {}).get('language', 'it')
        
        help_text = {
            'it': """
📖 **GUIDA COMPLETA - GIGLIO DOWNLOAD**

🎯 **Piattaforme Supportate:**
• 📺 YouTube (Video + Audio)
• 📷 Instagram (Stories, Reels, Posts)
• 🎵 TikTok (Video + Audio)
• 🐦 Twitter/X (Video + Audio)
• 👥 Facebook (Video + Audio)
• 🔴 Reddit (Video + Audio)
• 🎬 Vimeo (Video + Audio)
• 🔗 Link diretti (File, Immagini)

⚡ **Qualità Disponibili:**
• 🎬 Video 4K (1080p) - Massima qualità
• 🎥 Video HD (720p) - Alta qualità
• 📱 Video (480p) - Qualità media
• 🎵 MP3 Premium (320kbps) - Audio perfetto
• 🎵 MP3 Qualità (192kbps) - Audio buono
• ⚡ MP3 Veloce (128kbps) - Download veloce

🚀 **Come Usare:**
1. Invia un link da qualsiasi piattaforma
2. Scegli la qualità preferita
3. Scarica e goditi il contenuto!

💡 **Suggerimenti:**
• I link YouTube funzionano anche con playlist
• Supporta link Instagram, TikTok, Twitter
• Download paralleli per velocità massima
• Qualità automatica se disponibile

❓ **Problemi?** Usa /support per assistenza
            """,
            'en': """
📖 **COMPLETE GUIDE - GIGLIO DOWNLOAD**

🎯 **Supported Platforms:**
• 📺 YouTube (Video + Audio)
• 📷 Instagram (Stories, Reels, Posts)
• 🎵 TikTok (Video + Audio)
• 🐦 Twitter/X (Video + Audio)
• 👥 Facebook (Video + Audio)
• 🔴 Reddit (Video + Audio)
• 🎬 Vimeo (Video + Audio)
• 🔗 Direct links (Files, Images)

⚡ **Available Qualities:**
• 🎬 Video 4K (1080p) - Maximum quality
• 🎥 Video HD (720p) - High quality
• 📱 Video (480p) - Medium quality
• 🎵 MP3 Premium (320kbps) - Perfect audio
• 🎵 MP3 Quality (192kbps) - Good audio
• ⚡ MP3 Fast (128kbps) - Fast download

🚀 **How to Use:**
1. Send a link from any platform
2. Choose your preferred quality
3. Download and enjoy!

💡 **Tips:**
• YouTube links work with playlists too
• Supports Instagram, TikTok, Twitter links
• Parallel downloads for maximum speed
• Automatic quality if available

❓ **Issues?** Use /support for assistance
            """
        }
        
        await update.message.reply_text(help_text[lang], parse_mode='Markdown')
    
    async def support_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /support per assistenza"""
        user_id = update.effective_user.id
        lang = self.user_sessions.get(user_id, {}).get('language', 'it')
        
        support_text = {
            'it': """
🆘 **SUPPORTO TECNICO**

❓ **Problemi Comuni:**
• Link non riconosciuto → Prova un link diverso
• Download lento → Scegli qualità più bassa
• Errore YouTube → Riprova tra qualche minuto
• File troppo grande → Scegli formato audio

🔧 **Soluzioni:**
• Riavvia il bot con /start
• Controlla che il link sia corretto
• Prova con un altro link della stessa piattaforma

📞 **Contatto:**
Per problemi urgenti, contatta l'amministratore.

💡 **Suggerimento:** Il bot funziona meglio con link pubblici!
            """,
            'en': """
🆘 **TECHNICAL SUPPORT**

❓ **Common Issues:**
• Link not recognized → Try a different link
• Slow download → Choose lower quality
• YouTube error → Try again in a few minutes
• File too large → Choose audio format

🔧 **Solutions:**
• Restart bot with /start
• Check that the link is correct
• Try with another link from the same platform

📞 **Contact:**
For urgent issues, contact the administrator.

💡 **Tip:** The bot works better with public links!
            """
        }
        
        await update.message.reply_text(support_text[lang], parse_mode='Markdown')
    
    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestisce selezione lingua"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        lang = query.data.split('_')[1]
        
        # Aggiorna sessione utente
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        self.user_sessions[user_id]['language'] = lang
        
        welcome_text = {
            'it': """
🎵 **BENVENUTO IN GIGLIO DOWNLOAD UNLIMITED!** 🎵
*Il migliore downloader in circolazione!*

🚀 **Funzionalità:**
• 📺 YouTube (Video + Audio)
• 📷 Instagram (Stories, Reels)
• 🎵 TikTok (Video + Audio)
• 🐦 Twitter/X (Video + Audio)
• 👥 Facebook (Video + Audio)
• 🔴 Reddit (Video + Audio)
• 🎬 Vimeo (Video + Audio)

⚡ **Qualità Disponibili:**
• 🎬 Video 4K (1080p)
• 🎥 Video HD (720p)
• 📱 Video (480p)
• 🎵 MP3 Premium (320kbps)
• 🎵 MP3 Qualità (192kbps)
• ⚡ MP3 Veloce (128kbps)

📖 **Comandi:**
/help - Guida completa
/support - Assistenza tecnica

🎯 **Invia un link per iniziare!**
            """,
            'en': """
🎵 **WELCOME TO GIGLIO DOWNLOAD UNLIMITED!** 🎵
*The best downloader in circulation!*

🚀 **Features:**
• 📺 YouTube (Video + Audio)
• 📷 Instagram (Stories, Reels)
• 🎵 TikTok (Video + Audio)
• 🐦 Twitter/X (Video + Audio)
• 👥 Facebook (Video + Audio)
• 🔴 Reddit (Video + Audio)
• 🎬 Vimeo (Video + Audio)

⚡ **Available Qualities:**
• 🎬 Video 4K (1080p)
• 🎥 Video HD (720p)
• 📱 Video (480p)
• 🎵 MP3 Premium (320kbps)
• 🎵 MP3 Quality (192kbps)
• ⚡ MP3 Fast (128kbps)

📖 **Commands:**
/help - Complete guide
/support - Technical support

🎯 **Send a link to get started!**
            """
        }
        
        await query.edit_message_text(welcome_text[lang], parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestisce messaggi in arrivo"""
        message = update.message
        user_id = update.effective_user.id
        lang = self.user_sessions.get(user_id, {}).get('language', 'it')
        
        # Controlla se è un URL
        if message.text and self._is_url(message.text):
            await self._handle_url(message, context, lang)
        elif message.document or message.photo or message.video or message.audio:
            await self._handle_file(message, context, lang)
        else:
            await message.reply_text(
                MESSAGES['help'][lang],
                parse_mode='Markdown'
            )
    
    def _is_url(self, text: str) -> bool:
        """Controlla se il testo contiene un URL valido"""
        url_pattern = re.compile(
            r'https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?].*)?$', re.IGNORECASE)  # Allow any path and parameters
        
        return url_pattern.match(text) is not None
    
    async def _handle_url(self, message, context, lang):
        """Gestisce download da URL"""
        url = message.text
        
        # Messaggio di processing
        processing_text = {
            'it': "🔍 **Analizzando il link...**\n⏳ *Preparando le opzioni di download*",
            'en': "🔍 **Analyzing link...**\n⏳ *Preparing download options*"
        }
        
        processing_msg = await message.reply_text(processing_text[lang], parse_mode='Markdown')
        
        try:
            # Ottieni opzioni di download
            options = await self.downloader.get_download_options(url)
            
            if not options:
                error_text = {
                    'it': "❌ **Link non supportato**\n\nProva con un link da:\n• YouTube\n• Instagram\n• TikTok\n• Twitter\n• Facebook\n• Reddit\n• Vimeo",
                    'en': "❌ **Unsupported link**\n\nTry with a link from:\n• YouTube\n• Instagram\n• TikTok\n• Twitter\n• Facebook\n• Reddit\n• Vimeo"
                }
                await processing_msg.edit_text(error_text[lang], parse_mode='Markdown')
                return
            
            # Crea tastiera con opzioni
            keyboard = []
            for i, option in enumerate(options):
                keyboard.append([InlineKeyboardButton(
                    option['format'],
                    callback_data=f"download_{i}"
                )])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Messaggio con opzioni
            options_text = {
                'it': f"📥 **Trovate {len(options)} opzioni di download:**\n\n🎥 **Video** | 🎵 **Audio**\n\n**Scegli la qualità:**",
                'en': f"📥 **Found {len(options)} download options:**\n\n🎥 **Video** | 🎵 **Audio**\n\n**Select quality:**"
            }
            
            await processing_msg.edit_text(
                options_text[lang],
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Salva opzioni nel contesto
            context.user_data['download_options'] = options
            context.user_data['download_url'] = url
            
        except Exception as e:
            logger.error(f"Error processing URL: {e}")
            error_text = {
                'it': "❌ **Errore durante l'analisi**\n\nRiprova con un link diverso o contatta il supporto.",
                'en': "❌ **Error during analysis**\n\nTry again with a different link or contact support."
            }
            await processing_msg.edit_text(error_text[lang], parse_mode='Markdown')
    
    async def download_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestisce selezione qualità download"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        lang = self.user_sessions.get(user_id, {}).get('language', 'it')
        
        try:
            option_index = int(query.data.split('_')[1])
            options = context.user_data.get('download_options', [])
            url = context.user_data.get('download_url', '')
            
            if not options or option_index >= len(options):
                error_text = {
                    'it': "❌ **Opzione non valida**\n\nRiprova con un nuovo link.",
                    'en': "❌ **Invalid option**\n\nTry again with a new link."
                }
                await query.edit_message_text(error_text[lang], parse_mode='Markdown')
                return
            
            option = options[option_index]
            
            # Messaggio di download
            download_text = {
                'it': f"⬇️ **Download in corso...**\n\n🎯 **Qualità:** {option['format']}\n⏳ *Preparando il file...*",
                'en': f"⬇️ **Downloading...**\n\n🎯 **Quality:** {option['format']}\n⏳ *Preparing file...*"
            }
            
            await query.edit_message_text(download_text[lang], parse_mode='Markdown')
            
            # Download del file
            file_path = await self.downloader.download_file(url, option, user_id)
            
            if file_path:
                # Invia il file
                file_size = os.path.getsize(file_path)
                
                if file_size > MAX_FILE_SIZE:
                    error_text = {
                        'it': f"❌ **File troppo grande**\n\nDimensione: {format_file_size(file_size)}\nLimite: {format_file_size(MAX_FILE_SIZE)}\n\nScegli una qualità più bassa.",
                        'en': f"❌ **File too large**\n\nSize: {format_file_size(file_size)}\nLimit: {format_file_size(MAX_FILE_SIZE)}\n\nChoose a lower quality."
                    }
                    await query.edit_message_text(error_text[lang], parse_mode='Markdown')
                else:
                    # Invia il file
                    with open(file_path, 'rb') as file:
                        if option['type'] == 'video':
                            await context.bot.send_video(
                                chat_id=query.message.chat_id,
                                video=file,
                                caption=f"✅ **Download completato!**\n\n🎯 **Qualità:** {option['format']}",
                                parse_mode='Markdown'
                            )
                        else:
                            await context.bot.send_audio(
                                chat_id=query.message.chat_id,
                                audio=file,
                                caption=f"✅ **Download completato!**\n\n🎯 **Qualità:** {option['format']}",
                                parse_mode='Markdown'
                            )
                    
                    # Pulisci file temporaneo
                    try:
                        os.remove(file_path)
                    except:
                        pass
                    
                    success_text = {
                        'it': "✅ **Download completato con successo!**\n\n🎉 *Goditi il tuo contenuto!*",
                        'en': "✅ **Download completed successfully!**\n\n🎉 *Enjoy your content!*"
                    }
                    await query.edit_message_text(success_text[lang], parse_mode='Markdown')
            else:
                error_text = {
                    'it': "❌ **Errore durante il download**\n\nRiprova o scegli una qualità diversa.",
                    'en': "❌ **Error during download**\n\nTry again or choose a different quality."
                }
                await query.edit_message_text(error_text[lang], parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"Download error: {e}")
            error_text = {
                'it': "❌ **Errore imprevisto**\n\nRiprova o contatta il supporto.",
                'en': "❌ **Unexpected error**\n\nTry again or contact support."
            }
            await query.edit_message_text(error_text[lang], parse_mode='Markdown')
    
    async def _handle_file(self, message, context, lang):
        """Gestisce upload di file"""
        # Implementazione per gestire file uploadati
        await message.reply_text(
            "📁 **File ricevuto!**\n\nQuesta funzionalità sarà disponibile presto.",
            parse_mode='Markdown'
        )
    
    def run(self):
        """Avvia il bot"""
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found! Please set it in your environment variables.")
            return
        
        # Crea applicazione
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Aggiungi handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("support", self.support_command))
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(self.download_callback, pattern="^download_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, self.handle_message))
        
        # Avvia bot
        logger.info("🚀 Starting Professional Giglio Download Unlimited Bot...")
        application.run_polling()

if __name__ == "__main__":
    bot = ProfessionalBot()
    bot.run()
