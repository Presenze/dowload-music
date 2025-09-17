import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, MESSAGES, SUPPORTED_PLATFORMS, MAX_FILE_SIZE
from downloader import DownloadManager
from utils import detect_platform, get_file_type, format_file_size

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GiglioDownloadBot:
    def __init__(self):
        self.download_manager = DownloadManager()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🌍 Choose your language / Scegli la tua lingua:",
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        lang = context.user_data.get('language', 'en')
        await update.message.reply_text(MESSAGES['help'][lang])
    
    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        
        lang = query.data.split('_')[1]
        context.user_data['language'] = lang
        
        await query.edit_message_text(MESSAGES['start'][lang])
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        message = update.message
        lang = context.user_data.get('language', 'en')
        
        # Check if message contains a URL
        if message.text and any(platform in message.text.lower() for platform in SUPPORTED_PLATFORMS):
            await self.handle_url(message, context, lang)
        elif message.document or message.photo or message.video or message.audio:
            await self.handle_file(message, context, lang)
        else:
            await message.reply_text(MESSAGES['help'][lang])
    
    async def handle_url(self, message, context, lang):
        """Handle URL downloads"""
        url = message.text
        platform = detect_platform(url)
        
        if not platform:
            await message.reply_text(MESSAGES['error'][lang])
            return
        
        # Send processing message
        processing_msg = await message.reply_text(MESSAGES['processing'][lang])
        
        try:
            # Get download options
            options = await self.download_manager.get_download_options(url, platform)
            
            if not options:
                await processing_msg.edit_text(MESSAGES['error'][lang])
                return
            
            # Create quality selection keyboard
            keyboard = []
            for i, option in enumerate(options[:12]):  # Show up to 12 options
                quality_text = f"{option['format']} - {option['size']}"
                keyboard.append([InlineKeyboardButton(quality_text, callback_data=f"download_{i}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Get language-specific message
            if lang == 'it':
                message_text = f"📥 Trovate {len(options)} opzioni di download:\n\n🎥 Video | 🎵 Audio\n\nScegli la qualità:"
            else:
                message_text = f"📥 Found {len(options)} download options:\n\n🎥 Video | 🎵 Audio\n\nSelect quality:"
            
            await processing_msg.edit_text(message_text, reply_markup=reply_markup)
            
            # Store options in context
            context.user_data['download_options'] = options
            context.user_data['download_url'] = url
            
        except Exception as e:
            logger.error(f"Error processing URL: {e}")
            # Check if it's a YouTube sign-in error
            if "Please sign in" in str(e) or "Precondition check failed" in str(e):
                await processing_msg.edit_text(MESSAGES['youtube_error'][lang])
            else:
                await processing_msg.edit_text(MESSAGES['error'][lang])
    
    async def handle_file(self, message, context, lang):
        """Handle file uploads"""
        try:
            if message.document:
                file = message.document
            elif message.photo:
                file = message.photo[-1]  # Get highest resolution
            elif message.video:
                file = message.video
            elif message.audio:
                file = message.audio
            else:
                await message.reply_text(MESSAGES['error'][lang])
                return
            
            # Check file size
            if file.file_size > MAX_FILE_SIZE:
                lang = context.user_data.get('language', 'en')
                await message.reply_text(
                    f"{MESSAGES['file_too_large'][lang]} {format_file_size(MAX_FILE_SIZE)}"
                )
                return
            
            # Download file
            file_obj = await context.bot.get_file(file.file_id)
            file_path = f"downloads/{file.file_name or f'file_{file.file_id}'}"
            
            os.makedirs("downloads", exist_ok=True)
            await file_obj.download_to_drive(file_path)
            
            lang = context.user_data.get('language', 'en')
            await message.reply_text(
                f"{MESSAGES['file_saved'][lang]}\n📁 Percorso: {file_path}\n📊 Dimensione: {format_file_size(file.file_size)}"
            )
            
        except Exception as e:
            logger.error(f"Error handling file: {e}")
            await message.reply_text(MESSAGES['error'][lang])
    
    async def download_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle download quality selection"""
        query = update.callback_query
        await query.answer()
        
        lang = context.user_data.get('language', 'en')
        option_index = int(query.data.split('_')[1])
        
        options = context.user_data.get('download_options', [])
        url = context.user_data.get('download_url', '')
        
        if not options or not url:
            await query.edit_message_text(MESSAGES['error'][lang])
            return
        
        selected_option = options[option_index]
        
        # Start download
        lang = context.user_data.get('language', 'en')
        await query.edit_message_text(MESSAGES['downloading'][lang])
        
        try:
            file_path = await self.download_manager.download_file(
                url, selected_option, context.user_data.get('user_id', 0)
            )
            
            if file_path:
                # Send file to user
                with open(file_path, 'rb') as file:
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=file,
                        filename=os.path.basename(file_path)
                    )
                
                # Clean up
                os.remove(file_path)
                await query.edit_message_text(MESSAGES['download_complete'][lang])
            else:
                await query.edit_message_text(MESSAGES['error'][lang])
                
        except Exception as e:
            logger.error(f"Download error: {e}")
            await query.edit_message_text(MESSAGES['error'][lang])
    
    def run(self):
        """Start the bot"""
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found! Please set it in your environment variables.")
            return
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(self.download_callback, pattern="^download_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, self.handle_message))
        
        # Start bot
        logger.info("Starting Giglio Download Unlimited Bot...")
        application.run_polling()

if __name__ == "__main__":
    bot = GiglioDownloadBot()
    bot.run()
