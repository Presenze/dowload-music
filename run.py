#!/usr/bin/env python3
"""
Giglio Download Unlimited Bot
Main entry point for running the bot
"""

import os
import sys
import logging
from bot import GiglioDownloadBot
from config import BOT_TOKEN

def main():
    """Main function to run the bot"""
    # Check if BOT_TOKEN is set
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN not found!")
        print("Please check your config.py file or set the environment variable.")
        sys.exit(1)
    
    # Create downloads directory
    os.makedirs('downloads', exist_ok=True)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🌸 Starting Giglio Download Unlimited Bot...")
    
    try:
        # Create and run bot
        bot = GiglioDownloadBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
