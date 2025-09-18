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
from search_generator import SearchGenerator
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
        self.search_generator = SearchGenerator()
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
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🔍 Ricerca Musica", callback_data="search_music")],
            [InlineKeyboardButton("🎬 Ricerca Video", callback_data="search_video")],
            [InlineKeyboardButton("🎨 Crea Logo", callback_data="create_logo")],
            [InlineKeyboardButton("🖼️ Genera Immagine", callback_data="create_image")],
            [InlineKeyboardButton("📝 Immagine con Testo", callback_data="text_image")],
            [InlineKeyboardButton("❓ Aiuto Ricerca", callback_data="search_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = """
🎵 **GIGLIO DOWNLOAD UNLIMITED** 🎵
*Il migliore downloader in circolazione!*

🌍 **Scegli la tua lingua / Choose your language:**

🔍 **NUOVE FUNZIONI:**
• Ricerca musica e video
• Generazione logo e immagini
• Creazione contenuti personalizzati
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
        elif message.text:
            # Gestisce messaggi di ricerca
            await self._handle_search_message(message, context, lang)
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
    
    async def _handle_search_message(self, message, context, lang):
        """Gestisce messaggi di ricerca"""
        user_id = message.from_user.id
        text = message.text.strip()
        
        # Controlla se l'utente ha cliccato su un tasto di ricerca
        if user_id in self.user_sessions:
            session = self.user_sessions[user_id]
            
            # Se l'utente ha cliccato su ricerca musica
            if 'search_type' in session and session['search_type'] == 'music':
                await message.reply_text(f"🔍 Cerco musica per: **{text}**...")
                results = await self.search_generator.search_music(text, 10)
                if results:
                    message_text = self.search_generator.format_search_results(results, "musica")
                    await message.reply_text(message_text, parse_mode='Markdown')
                else:
                    await message.reply_text(f"❌ Nessuna musica trovata per: **{text}**")
                # Reset search type
                session.pop('search_type', None)
                return
            
            # Se l'utente ha cliccato su ricerca video
            elif 'search_type' in session and session['search_type'] == 'video':
                await message.reply_text(f"🔍 Cerco video per: **{text}**...")
                results = await self.search_generator.search_videos(text, 10)
                if results:
                    message_text = self.search_generator.format_search_results(results, "video")
                    await message.reply_text(message_text, parse_mode='Markdown')
                else:
                    await message.reply_text(f"❌ Nessun video trovato per: **{text}**")
                # Reset search type
                session.pop('search_type', None)
                return
            
            # Se l'utente ha cliccato su crea logo
            elif 'search_type' in session and session['search_type'] == 'logo':
                await message.reply_text(f"🎨 Creo logo per: **{text}**...")
                logo_url = await self.search_generator.generate_logo(text, "modern")
                if logo_url:
                    await message.reply_photo(
                        photo=logo_url,
                        caption=f"🎨 **Logo creato!**\n\nTesto: **{text}**\n\n💡 *Logo generato con stile moderno*"
                    )
                else:
                    await message.reply_text("❌ Errore durante la creazione del logo.")
                # Reset search type
                session.pop('search_type', None)
                return
            
            # Se l'utente ha cliccato su crea immagine
            elif 'search_type' in session and session['search_type'] == 'image':
                await message.reply_text(f"🖼️ Creo immagine per: **{text}**...")
                image_url = await self.search_generator.generate_image(text, "artistic")
                if image_url:
                    await message.reply_photo(
                        photo=image_url,
                        caption=f"🖼️ **Immagine creata!**\n\nPrompt: **{text}**\n\n💡 *Immagine generata con AI*"
                    )
                else:
                    await message.reply_text("❌ Errore durante la creazione dell'immagine.")
                # Reset search type
                session.pop('search_type', None)
                return
            
            # Se l'utente ha cliccato su immagine con testo
            elif 'search_type' in session and session['search_type'] == 'text_image':
                await message.reply_text(f"📝 Creo immagine con testo: **{text}**...")
                image_url = await self.search_generator.create_text_image(text, "blue", "white")
                if image_url:
                    await message.reply_photo(
                        photo=image_url,
                        caption=f"📝 **Immagine con testo creata!**\n\nTesto: **{text}**\n\n💡 *Immagine personalizzata*"
                    )
                else:
                    await message.reply_text("❌ Errore durante la creazione dell'immagine.")
                # Reset search type
                session.pop('search_type', None)
                return
        
        # Se non è una ricerca, mostra messaggio di aiuto
        help_text = {
            'it': "❓ **Come usare il bot:**\n\n🔗 **Per scaricare:** Invia un link\n🔍 **Per cercare:** Usa i tasti del menu\n\n📖 Usa /help per la guida completa",
            'en': "❓ **How to use the bot:**\n\n🔗 **To download:** Send a link\n🔍 **To search:** Use menu buttons\n\n📖 Use /help for complete guide"
        }
        await message.reply_text(help_text[lang], parse_mode='Markdown')
    
    async def search_music_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando per cercare musica"""
        try:
            query = ' '.join(context.args) if context.args else None
            if not query:
                await update.message.reply_text("🎵 **Ricerca Musica**\n\nUsa: `/search_music [nome canzone o artista]`\n\nEsempio: `/search_music Ed Sheeran Shape of You`")
                return
            
            await update.message.reply_text(f"🔍 Cerco musica per: **{query}**...")
            
            results = await self.search_generator.search_music(query, 10)
            if results:
                message = self.search_generator.format_search_results(results, "musica")
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(f"❌ Nessuna musica trovata per: **{query}**")
                
        except Exception as e:
            logger.error(f"Search music error: {e}")
            await update.message.reply_text("❌ Errore durante la ricerca musica.")
    
    async def search_video_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando per cercare video"""
        try:
            query = ' '.join(context.args) if context.args else None
            if not query:
                await update.message.reply_text("🎬 **Ricerca Video**\n\nUsa: `/search_video [tema o argomento]`\n\nEsempio: `/search_video tutorial cucina`")
                return
            
            await update.message.reply_text(f"🔍 Cerco video per: **{query}**...")
            
            results = await self.search_generator.search_videos(query, 10)
            if results:
                message = self.search_generator.format_search_results(results, "video")
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(f"❌ Nessun video trovato per: **{query}**")
                
        except Exception as e:
            logger.error(f"Search video error: {e}")
            await update.message.reply_text("❌ Errore durante la ricerca video.")
    
    async def create_logo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando per creare logo"""
        try:
            text = ' '.join(context.args) if context.args else None
            if not text:
                await update.message.reply_text("🎨 **Crea Logo**\n\nUsa: `/create_logo [testo del logo]`\n\nEsempio: `/create_logo La Mia Azienda`")
                return
            
            await update.message.reply_text(f"🎨 Creo logo per: **{text}**...")
            
            logo_url = await self.search_generator.generate_logo(text, "modern")
            if logo_url:
                await update.message.reply_photo(
                    photo=logo_url,
                    caption=f"🎨 **Logo creato!**\n\nTesto: **{text}**\n\n💡 *Logo generato con stile moderno*"
                )
            else:
                await update.message.reply_text("❌ Errore durante la creazione del logo.")
                
        except Exception as e:
            logger.error(f"Create logo error: {e}")
            await update.message.reply_text("❌ Errore durante la creazione del logo.")
    
    async def create_image_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando per creare immagine"""
        try:
            prompt = ' '.join(context.args) if context.args else None
            if not prompt:
                await update.message.reply_text("🖼️ **Crea Immagine**\n\nUsa: `/create_image [descrizione]`\n\nEsempio: `/create_image gatto che suona la chitarra`")
                return
            
            await update.message.reply_text(f"🖼️ Creo immagine per: **{prompt}**...")
            
            image_url = await self.search_generator.generate_image(prompt, "artistic")
            if image_url:
                await update.message.reply_photo(
                    photo=image_url,
                    caption=f"🖼️ **Immagine creata!**\n\nPrompt: **{prompt}**\n\n💡 *Immagine generata con AI*"
                )
            else:
                await update.message.reply_text("❌ Errore durante la creazione dell'immagine.")
                
        except Exception as e:
            logger.error(f"Create image error: {e}")
            await update.message.reply_text("❌ Errore durante la creazione dell'immagine.")
    
    async def text_image_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando per creare immagine con testo"""
        try:
            text = ' '.join(context.args) if context.args else None
            if not text:
                await update.message.reply_text("📝 **Crea Immagine con Testo**\n\nUsa: `/text_image [testo]`\n\nEsempio: `/text_image Benvenuti`")
                return
            
            await update.message.reply_text(f"📝 Creo immagine con testo: **{text}**...")
            
            image_url = await self.search_generator.create_text_image(text, "blue", "white")
            if image_url:
                await update.message.reply_photo(
                    photo=image_url,
                    caption=f"📝 **Immagine con testo creata!**\n\nTesto: **{text}**\n\n💡 *Immagine personalizzata*"
                )
            else:
                await update.message.reply_text("❌ Errore durante la creazione dell'immagine.")
                
        except Exception as e:
            logger.error(f"Text image error: {e}")
            await update.message.reply_text("❌ Errore durante la creazione dell'immagine.")
    
    async def search_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando di aiuto per le funzioni di ricerca"""
        try:
            help_text = self.search_generator.get_search_help()
            await update.message.reply_text(help_text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Search help error: {e}")
            await update.message.reply_text("❌ Errore durante il caricamento dell'aiuto.")
    
    async def search_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback per tasti di ricerca"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        
        if query.data == "search_music":
            self.user_sessions[user_id]['search_type'] = 'music'
            await query.edit_message_text(
                "🎵 **Ricerca Musica**\n\nInvia il nome della canzone o artista che vuoi cercare.\n\nEsempio: `Ed Sheeran Shape of You`",
                parse_mode='Markdown'
            )
        elif query.data == "search_video":
            self.user_sessions[user_id]['search_type'] = 'video'
            await query.edit_message_text(
                "🎬 **Ricerca Video**\n\nInvia il tema o argomento che vuoi cercare.\n\nEsempio: `tutorial cucina italiana`",
                parse_mode='Markdown'
            )
    
    async def create_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback per tasti di creazione"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        
        if query.data == "create_logo":
            self.user_sessions[user_id]['search_type'] = 'logo'
            await query.edit_message_text(
                "🎨 **Crea Logo**\n\nInvia il testo che vuoi nel logo.\n\nEsempio: `La Mia Azienda`",
                parse_mode='Markdown'
            )
        elif query.data == "create_image":
            self.user_sessions[user_id]['search_type'] = 'image'
            await query.edit_message_text(
                "🖼️ **Genera Immagine**\n\nInvia una descrizione dell'immagine che vuoi creare.\n\nEsempio: `gatto che suona la chitarra`",
                parse_mode='Markdown'
            )
    
    async def text_image_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback per immagine con testo"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        
        self.user_sessions[user_id]['search_type'] = 'text_image'
        await query.edit_message_text(
            "📝 **Crea Immagine con Testo**\n\nInvia il testo che vuoi nell'immagine.\n\nEsempio: `Benvenuti`",
            parse_mode='Markdown'
        )
    
    async def search_help_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback per aiuto ricerca"""
        query = update.callback_query
        await query.answer()
        
        help_text = self.search_generator.get_search_help()
        await query.edit_message_text(help_text, parse_mode='Markdown')
    
    def run(self):
        """Avvia il bot con gestione conflitti"""
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found! Please set it in your environment variables.")
            return
        
        # Crea applicazione con gestione conflitti
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Configura polling per evitare conflitti
        application.bot_data['get_updates_request'] = {
            'timeout': 30,
            'read_timeout': 30,
            'write_timeout': 30,
            'connect_timeout': 30,
            'pool_timeout': 30,
        }
        
        # Aggiungi handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("support", self.support_command))
        
        # Nuovi comandi di ricerca e generazione
        application.add_handler(CommandHandler("search_music", self.search_music_command))
        application.add_handler(CommandHandler("search_video", self.search_video_command))
        application.add_handler(CommandHandler("create_logo", self.create_logo_command))
        application.add_handler(CommandHandler("create_image", self.create_image_command))
        application.add_handler(CommandHandler("text_image", self.text_image_command))
        application.add_handler(CommandHandler("search_help", self.search_help_command))
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(self.download_callback, pattern="^download_"))
        application.add_handler(CallbackQueryHandler(self.search_callback, pattern="^search_"))
        application.add_handler(CallbackQueryHandler(self.create_callback, pattern="^create_"))
        application.add_handler(CallbackQueryHandler(self.text_image_callback, pattern="^text_image"))
        application.add_handler(CallbackQueryHandler(self.search_help_callback, pattern="^search_help"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, self.handle_message))
        
        # Avvia bot con retry per conflitti
        logger.info("🚀 Starting Professional Giglio Download Unlimited Bot...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                application.run_polling(
                    timeout=30,
                    read_timeout=30,
                    write_timeout=30,
                    connect_timeout=30,
                    pool_timeout=30,
                    drop_pending_updates=True  # Drop pending updates to avoid conflicts
                )
                break
            except Exception as e:
                if "Conflict" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"Bot conflict detected (attempt {attempt + 1}/{max_retries}). Retrying in 5 seconds...")
                    import time
                    time.sleep(5)
                    continue
                else:
                    logger.error(f"Failed to start bot after {max_retries} attempts: {e}")
                    raise

if __name__ == "__main__":
    bot = ProfessionalBot()
    bot.run()
