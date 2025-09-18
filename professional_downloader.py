#!/usr/bin/env python3
"""
Professional Downloader - Il migliore downloader in circolazione
Supporta TUTTE le piattaforme con qualità massima e velocità
"""

import os
import re
import asyncio
import logging
import aiohttp
import aiofiles
from typing import List, Dict, Optional, Union
import yt_dlp
from urllib.parse import urlparse, parse_qs
import json
import time

logger = logging.getLogger(__name__)

class ProfessionalDownloader:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Configurazione professionale per massima qualità e velocità
        self.ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': True,
            'writeinfojson': False,
            'extractor_retries': 3,
            'fragment_retries': 3,
            'retries': 3,
            'socket_timeout': 15,  # Timeout più veloce
            'http_chunk_size': 4194304,  # 4MB chunks per velocità massima
            'concurrent_fragment_downloads': 16,  # 16 download paralleli
            'fragment_retries': 2,  # Meno retry per velocità
            'skip_unavailable_fragments': True,
            'retries': 2,  # Meno retry totali
            # Configurazioni avanzate
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # FFmpeg settings
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'merge_output_format': 'mp4',
            'prefer_ffmpeg': True,
            # YouTube specific - Aggressive bypass
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web', 'ios', 'android_music', 'android_creator'],
                    'skip': ['translated_subs', 'dash', 'hls'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            },
            # Bypass authentication
            'cookiesfrombrowser': None,
            'no_check_certificate': True,
            'prefer_insecure': True,
            'sleep_interval': 1,
            'max_sleep_interval': 5,
        }
        
        # Piattaforme supportate con configurazioni specifiche
        self.platforms = {
            'youtube': {
                'domains': ['youtube.com', 'youtu.be', 'music.youtube.com'],
                'formats': ['best[height<=1080]/best[height<=720]/best[height<=480]/best', 'bestaudio[abr<=320]/bestaudio[abr<=192]/bestaudio'],
                'quality_options': [
                    {'id': '1080p', 'name': '🎬 Video 4K (1080p)', 'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best'},
                    {'id': '720p', 'name': '🎥 Video HD (720p)', 'format': 'best[height<=720]/best[height<=480]/best'},
                    {'id': '480p', 'name': '📱 Video (480p)', 'format': 'best[height<=480]/best'},
                    {'id': 'audio_320', 'name': '🎵 MP3 Premium (320kbps)', 'format': 'bestaudio[abr<=320]/bestaudio[abr<=192]/bestaudio'},
                    {'id': 'audio_192', 'name': '🎵 MP3 Qualità (192kbps)', 'format': 'bestaudio[abr<=192]/bestaudio'},
                    {'id': 'audio_128', 'name': '⚡ MP3 Veloce (128kbps)', 'format': 'bestaudio/worstaudio[abr>=128]'},
                ]
            },
            'instagram': {
                'domains': ['instagram.com'],
                'formats': ['best'],
                'quality_options': [
                    {'id': 'best', 'name': '📷 Video/Photo (Migliore Qualità)', 'format': 'best'},
                    {'id': 'audio', 'name': '🎵 Solo Audio', 'format': 'bestaudio'},
                ]
            },
            'tiktok': {
                'domains': ['tiktok.com', 'vm.tiktok.com'],
                'formats': ['best'],
                'quality_options': [
                    {'id': 'best', 'name': '🎵 TikTok Video (HD)', 'format': 'best'},
                    {'id': 'audio', 'name': '🎵 Solo Audio', 'format': 'bestaudio'},
                ]
            },
            'twitter': {
                'domains': ['twitter.com', 'x.com'],
                'formats': ['best'],
                'quality_options': [
                    {'id': 'best', 'name': '🐦 Tweet Video (HD)', 'format': 'best'},
                    {'id': 'audio', 'name': '🎵 Solo Audio', 'format': 'bestaudio'},
                ]
            },
            'facebook': {
                'domains': ['facebook.com', 'fb.watch'],
                'formats': ['best'],
                'quality_options': [
                    {'id': 'best', 'name': '👥 Facebook Video (HD)', 'format': 'best'},
                    {'id': 'audio', 'name': '🎵 Solo Audio', 'format': 'bestaudio'},
                ]
            },
            'reddit': {
                'domains': ['reddit.com'],
                'formats': ['best'],
                'quality_options': [
                    {'id': 'best', 'name': '🔴 Reddit Video (HD)', 'format': 'best'},
                    {'id': 'audio', 'name': '🎵 Solo Audio', 'format': 'bestaudio'},
                ]
            },
            'vimeo': {
                'domains': ['vimeo.com'],
                'formats': ['best'],
                'quality_options': [
                    {'id': 'best', 'name': '🎬 Vimeo Video (HD)', 'format': 'best'},
                    {'id': 'audio', 'name': '🎵 Solo Audio', 'format': 'bestaudio'},
                ]
            }
        }
    
    def detect_platform(self, url: str) -> Optional[str]:
        """Rileva la piattaforma dal URL"""
        url_lower = url.lower()
        
        for platform, config in self.platforms.items():
            for domain in config['domains']:
                if domain in url_lower:
                    return platform
        
        return None
    
    async def get_download_options(self, url: str) -> List[Dict]:
        """Ottieni opzioni di download per qualsiasi URL"""
        try:
            platform = self.detect_platform(url)
            
            if not platform:
                return await self._get_generic_options(url)
            
            # YouTube specific handling - Use revolutionary bypass
            if platform == 'youtube':
                from youtube_revolution import YouTubeRevolution
                youtube_revolution = YouTubeRevolution()
                return await youtube_revolution.get_download_options(url)
            
            # Usa configurazione specifica per la piattaforma
            return await self._get_platform_options(url, platform)
            
        except Exception as e:
            logger.error(f"Error getting options: {e}")
            return self._get_fallback_options()
    
    async def _get_platform_options(self, url: str, platform: str) -> List[Dict]:
        """Ottieni opzioni specifiche per la piattaforma"""
        try:
            # Configurazione specifica per la piattaforma
            opts = self.ydl_opts.copy()
            
            if platform == 'youtube':
                # YouTube: usa configurazione avanzata
                opts.update({
                    'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web', 'ios'],
                            'skip': ['translated_subs'],
                        }
                    },
                })
            else:
                # Altre piattaforme: usa formato migliore
                opts['format'] = 'best'
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return self._get_fallback_options()
                
                # Estrai informazioni
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                
                # Genera opzioni basate sulla piattaforma
                options = []
                platform_config = self.platforms[platform]
                
                for quality in platform_config['quality_options']:
                    options.append({
                        'format_id': quality['id'],
                        'format': quality['name'],
                        'size': f'{duration//60}min' if duration else 'Unknown',
                        'ext': 'mp4' if 'video' in quality['name'].lower() else 'mp3',
                        'type': 'video' if 'video' in quality['name'].lower() else 'audio',
                        'quality': quality['id'],
                        'title': title,
                        'uploader': uploader,
                        'platform': platform,
                        'ydl_format': quality['format']
                    })

                # Assicurati che le opzioni audio MP3 siano sempre presenti
                audio_present = any(opt['type'] == 'audio' for opt in options)
                if not audio_present:
                    options.extend([
                        {
                            'format_id': 'audio_320',
                            'format': '🎵 MP3 Premium (320kbps)',
                            'size': f'{duration//60}min' if duration else 'Unknown',
                            'ext': 'mp3',
                            'type': 'audio',
                            'quality': 'audio_320',
                            'title': title,
                            'uploader': uploader,
                            'platform': platform,
                            'ydl_format': 'bestaudio/best'
                        },
                        {
                            'format_id': 'audio_192',
                            'format': '🎵 MP3 Qualità (192kbps)',
                            'size': f'{duration//60}min' if duration else 'Unknown',
                            'ext': 'mp3',
                            'type': 'audio',
                            'quality': 'audio_192',
                            'title': title,
                            'uploader': uploader,
                            'platform': platform,
                            'ydl_format': 'bestaudio/best'
                        },
                        {
                            'format_id': 'audio_128',
                            'format': '⚡ MP3 Veloce (128kbps)',
                            'size': f'{duration//60}min' if duration else 'Unknown',
                            'ext': 'mp3',
                            'type': 'audio',
                            'quality': 'audio_128',
                            'title': title,
                            'uploader': uploader,
                            'platform': platform,
                            'ydl_format': 'worstaudio/worst'
                        }
                    ])
                
                return options
                
        except Exception as e:
            logger.error(f"Platform options error: {e}")
            return self._get_fallback_options()
    
    async def _get_generic_options(self, url: str) -> List[Dict]:
        """Ottieni opzioni per URL generici"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return self._get_fallback_options()
                
                title = info.get('title', 'Unknown Title')
                
                return [
                    {
                        'format_id': 'best',
                        'format': '🔗 Download Migliore Qualità',
                        'size': 'Unknown',
                        'ext': 'mp4',
                        'type': 'video',
                        'quality': 'best',
                        'title': title,
                        'platform': 'generic',
                        'ydl_format': 'best'
                    }
                ]
                
        except Exception as e:
            logger.error(f"Generic options error: {e}")
            return self._get_fallback_options()
    
    def _get_fallback_options(self) -> List[Dict]:
        """Opzioni di fallback sempre disponibili"""
        return [
            {
                'format_id': 'best',
                'format': '🎬 Video HD (Migliore Qualità)',
                'size': 'Alta qualità',
                'ext': 'mp4',
                'type': 'video',
                'quality': 'best',
                'platform': 'fallback',
                'ydl_format': 'best'
            },
            {
                'format_id': 'audio',
                'format': '🎵 MP3 Premium (320kbps)',
                'size': 'Audio premium',
                'ext': 'mp3',
                'type': 'audio',
                'quality': 'audio',
                'platform': 'fallback',
                'ydl_format': 'bestaudio'
            }
        ]
    
    async def download_file(self, url: str, option: Dict, user_id: int) -> Optional[str]:
        """Download file con l'opzione selezionata"""
        try:
            user_dir = os.path.join(self.download_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Configurazione per il download
            opts = self.ydl_opts.copy()
            opts['outtmpl'] = os.path.join(user_dir, '%(title)s.%(ext)s')
            opts['format'] = option.get('ydl_format', 'best')

            # Se audio MP3, forza estrazione con FFmpeg
            if option.get('type') == 'audio' or option.get('ext') == 'mp3':
                target_quality = '320'
                if '192' in option.get('format', ''):
                    target_quality = '192'
                elif '128' in option.get('format', ''):
                    target_quality = '128'

                opts.update({
                    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                    'postprocessors': [
                        {
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': target_quality,
                        }
                    ],
                    'ffmpeg_location': '/usr/bin/ffmpeg',
                    'prefer_ffmpeg': True,
                })
            else:
                # Preferisci formati progressivi MP4 quando possibile
                opts['format'] = f"bestvideo[ext=mp4][vcodec^=avc1][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/" + opts['format']
            
            # Download con timeout
            with yt_dlp.YoutubeDL(opts) as ydl:
                try:
                    ydl.download([url])
                except Exception as e:
                    logger.warning(f"Download failed: {e}, trying fallback...")
                    # Fallback: prova audio-only veloce
                    if option.get('type') != 'audio':
                        fallback_audio = self.ydl_opts.copy()
                        fallback_audio['outtmpl'] = os.path.join(user_dir, '%(title)s.%(ext)s')
                        fallback_audio.update({
                            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                            'postprocessors': [
                                {
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }
                            ],
                            'ffmpeg_location': '/usr/bin/ffmpeg',
                            'prefer_ffmpeg': True,
                        })
                        with yt_dlp.YoutubeDL(fallback_audio) as ydl_audio:
                            ydl_audio.download([url])
                
                # Trova il file scaricato
                for file in os.listdir(user_dir):
                    if any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mp3', '.m4a', '.avi', '.mkv']):
                        return os.path.join(user_dir, file)
                
                return None
                
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None
    
    async def get_video_info(self, url: str) -> Dict:
        """Ottieni informazioni dettagliate del video"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                    'thumbnail': info.get('thumbnail', ''),
                    'platform': self.detect_platform(url)
                }
                
        except Exception as e:
            logger.error(f"Info error: {e}")
            return {}

# Test function
async def test_professional_downloader():
    """Test del downloader professionale"""
    downloader = ProfessionalDownloader()
    
    test_urls = [
        "https://youtu.be/fJOE0vUjjo8?si=7P_VCMfO0wBwKq_Y",
        "https://www.youtube.com/watch?v=Q7NjUxGMv7Y&list=RDQ7NjUxGMv7Y&start_radio=1",
        "https://www.instagram.com/p/example/",
        "https://www.tiktok.com/@user/video/1234567890"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        platform = downloader.detect_platform(url)
        print(f"📱 Platform: {platform}")
        
        options = await downloader.get_download_options(url)
        print(f"✅ Options: {len(options)} found")
        
        for opt in options:
            print(f"   - {opt['format']} ({opt['type']})")

if __name__ == "__main__":
    asyncio.run(test_professional_downloader())
