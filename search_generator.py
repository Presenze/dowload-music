#!/usr/bin/env python3
"""
Giglio Download Unlimited Bot - Search & Generator Module
Funzioni di ricerca e generazione contenuti
"""

import os
import re
import asyncio
import logging
import aiohttp
import aiofiles
from typing import List, Dict, Optional, Union
import yt_dlp
from urllib.parse import quote_plus
import json
import time

logger = logging.getLogger(__name__)

class SearchGenerator:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Configurazione per ricerca YouTube
        self.search_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_music', 'android_creator', 'android'],
                    'skip': ['translated_subs', 'dash', 'hls'],
                }
            },
        }
    
    async def search_youtube(self, query: str, max_results: int = 10) -> List[Dict]:
        """Cerca video su YouTube"""
        try:
            results = []
            search_query = f"ytsearch{max_results}:{query}"
            
            with yt_dlp.YoutubeDL(self.search_opts) as ydl:
                search_results = ydl.extract_info(search_query, download=False)
                
                if search_results and 'entries' in search_results:
                    for entry in search_results['entries']:
                        if entry:
                            results.append({
                                'id': entry.get('id', ''),
                                'title': entry.get('title', 'Senza titolo'),
                                'uploader': entry.get('uploader', 'Sconosciuto'),
                                'duration': entry.get('duration', 0),
                                'view_count': entry.get('view_count', 0),
                                'url': f"https://youtube.com/watch?v={entry.get('id', '')}",
                                'thumbnail': entry.get('thumbnail', ''),
                            })
            
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    async def search_music(self, query: str, max_results: int = 10) -> List[Dict]:
        """Cerca musica specifica su YouTube"""
        try:
            # Aggiungi termini di ricerca per musica
            music_query = f"{query} music song audio"
            return await self.search_youtube(music_query, max_results)
        except Exception as e:
            logger.error(f"Music search error: {e}")
            return []
    
    async def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Cerca video generici su YouTube"""
        try:
            return await self.search_youtube(query, max_results)
        except Exception as e:
            logger.error(f"Video search error: {e}")
            return []
    
    async def generate_logo(self, text: str, style: str = "modern") -> Optional[str]:
        """Genera logo con testo (simulato - in produzione usare API reali)"""
        try:
            # Simulazione generazione logo
            # In produzione, integrare con API come Canva, Figma, o servizi AI
            logo_data = {
                'text': text,
                'style': style,
                'generated_at': time.time(),
                'url': f"https://via.placeholder.com/400x200/4CAF50/FFFFFF?text={quote_plus(text)}"
            }
            
            # Salva info logo
            logo_file = os.path.join(self.download_dir, f"logo_{int(time.time())}.json")
            async with aiofiles.open(logo_file, 'w') as f:
                await f.write(json.dumps(logo_data, indent=2))
            
            return logo_data['url']
            
        except Exception as e:
            logger.error(f"Logo generation error: {e}")
            return None
    
    async def generate_image(self, prompt: str, style: str = "artistic") -> Optional[str]:
        """Genera immagine da prompt (simulato - in produzione usare API reali)"""
        try:
            # Simulazione generazione immagine
            # In produzione, integrare con DALL-E, Midjourney, Stable Diffusion, etc.
            image_data = {
                'prompt': prompt,
                'style': style,
                'generated_at': time.time(),
                'url': f"https://picsum.photos/512/512?random={int(time.time())}"
            }
            
            # Salva info immagine
            image_file = os.path.join(self.download_dir, f"image_{int(time.time())}.json")
            async with aiofiles.open(image_file, 'w') as f:
                await f.write(json.dumps(image_data, indent=2))
            
            return image_data['url']
            
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return None
    
    async def create_text_image(self, text: str, background_color: str = "blue", text_color: str = "white") -> Optional[str]:
        """Crea immagine con testo personalizzato"""
        try:
            # Simulazione creazione immagine con testo
            # In produzione, usare PIL/Pillow per creare immagini reali
            text_clean = re.sub(r'[^\w\s]', '', text)[:20]  # Limita testo
            image_url = f"https://via.placeholder.com/600x300/{background_color.replace('#', '')}/{text_color.replace('#', '')}?text={quote_plus(text_clean)}"
            
            return image_url
            
        except Exception as e:
            logger.error(f"Text image creation error: {e}")
            return None
    
    def format_search_results(self, results: List[Dict], search_type: str = "video") -> str:
        """Formatta risultati di ricerca per Telegram"""
        if not results:
            return f"❌ Nessun {search_type} trovato. Prova con termini diversi."
        
        message = f"🔍 **Risultati per {search_type}:**\n\n"
        
        for i, result in enumerate(results[:5], 1):  # Mostra solo primi 5
            duration = f"{result['duration']//60}:{result['duration']%60:02d}" if result['duration'] else "N/A"
            views = f"{result['view_count']:,}" if result['view_count'] else "N/A"
            
            message += f"**{i}.** {result['title'][:60]}{'...' if len(result['title']) > 60 else ''}\n"
            message += f"👤 {result['uploader']}\n"
            message += f"⏱️ {duration} | 👁️ {views} views\n"
            message += f"🔗 [Guarda]({result['url']})\n\n"
        
        message += "💡 **Come usare:** Invia il link del video che vuoi scaricare!"
        return message
    
    def get_search_help(self) -> str:
        """Messaggio di aiuto per le funzioni di ricerca"""
        return """
🔍 **FUNZIONI DI RICERCA E GENERAZIONE**

**🎵 Ricerca Musica:**
• `/search_music [nome canzone]` - Cerca canzoni
• `/search_music [artista]` - Cerca per artista

**🎬 Ricerca Video:**
• `/search_video [tema]` - Cerca video generici
• `/search_video [tutorial]` - Cerca tutorial

**🎨 Generazione Contenuti:**
• `/create_logo [testo]` - Crea logo con testo
• `/create_image [descrizione]` - Genera immagine
• `/text_image [testo]` - Crea immagine con testo

**💡 Esempi:**
• `/search_music Ed Sheeran`
• `/search_video cucina italiana`
• `/create_logo La Mia Azienda`
• `/text_image Benvenuti`

**🚀 Funzioni Premium:**
• Download automatico dai risultati
• Generazione immagini AI
• Logo personalizzati
• Ricerca avanzata
        """
