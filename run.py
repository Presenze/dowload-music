#!/usr/bin/env python3
"""
Giglio Download Unlimited Bot
Main entry point for running the bot
"""

import os
import sys
import logging
import threading
import socketserver
import http.server
from professional_bot import ProfessionalBot
from config import BOT_TOKEN

class _HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        return

def _start_health_server():
    port = int(os.environ.get('PORT', '8080'))
    server = socketserver.TCPServer(('', port), _HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

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
    # Start lightweight HTTP healthcheck server for Railway
    _start_health_server()
    
    try:
        # Create and run bot
        bot = ProfessionalBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
