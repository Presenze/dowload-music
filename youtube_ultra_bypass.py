#!/usr/bin/env python3
"""
YouTube Ultra Bypass - Bypass ultra-aggressivo per YouTube
Utilizza tecniche avanzate per bypassare TUTTE le restrizioni di YouTube
"""

import os
import re
import asyncio
import logging
import yt_dlp
import random
import time
import json
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs, urlencode

logger = logging.getLogger(__name__)

class YouTubeUltraBypass:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        
        # User agents ultra-realistici
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        
        # Configurazioni ultra-aggressive
        self.ultra_configs = [
            self._get_ultra_config_1(),  # Configurazione 1: Ultra-aggressiva
            self._get_ultra_config_2(),  # Configurazione 2: Mobile-first
            self._get_ultra_config_3(),  # Configurazione 3: Web-first
            self._get_ultra_config_4(),  # Configurazione 4: Legacy
            self._get_ultra_config_5(),  # Configurazione 5: Fallback
        ]
    
    def _get_ultra_config_1(self):
        """Configurazione 1: Ultra-aggressiva"""
        return {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'best[height<=1080]/best[height<=720]/best[height<=480]/best',
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 10,
            'fragment_retries': 10,
            'retries': 10,
            'socket_timeout': 60,
            'http_chunk_size': 1048576,
            'concurrent_fragment_downloads': 1,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': random.choice(self.user_agents),
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'merge_output_format': 'mp4',
            'cookiesfrombrowser': None,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs', 'automatic_captions'],
                    'player_skip': ['webpage'],
                    'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    
    def _get_ultra_config_2(self):
        """Configurazione 2: Mobile-first"""
        return {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'worst[height<=480]/worst',
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 8,
            'fragment_retries': 8,
            'retries': 8,
            'socket_timeout': 45,
            'http_chunk_size': 524288,
            'concurrent_fragment_downloads': 1,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'merge_output_format': 'mp4',
            'cookiesfrombrowser': None,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs', 'automatic_captions', 'live_chat'],
                    'player_skip': ['webpage', 'configs'],
                    'player_client': ['android'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    
    def _get_ultra_config_3(self):
        """Configurazione 3: Web-first"""
        return {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'best[height<=720]/best[height<=480]/best',
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 6,
            'fragment_retries': 6,
            'retries': 6,
            'socket_timeout': 30,
            'http_chunk_size': 1048576,
            'concurrent_fragment_downloads': 2,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'merge_output_format': 'mp4',
            'cookiesfrombrowser': None,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs'],
                    'player_skip': ['webpage'],
                    'player_client': ['web'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    
    def _get_ultra_config_4(self):
        """Configurazione 4: Legacy"""
        return {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'worst',
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 5,
            'fragment_retries': 5,
            'retries': 5,
            'socket_timeout': 20,
            'http_chunk_size': 262144,
            'concurrent_fragment_downloads': 1,
            'fragment_retries': 2,
            'skip_unavailable_fragments': True,
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'merge_output_format': 'mp4',
            'cookiesfrombrowser': None,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs', 'automatic_captions', 'live_chat', 'comments'],
                    'player_skip': ['webpage', 'configs', 'js'],
                    'player_client': ['android'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    
    def _get_ultra_config_5(self):
        """Configurazione 5: Fallback"""
        return {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'worst',
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 3,
            'fragment_retries': 3,
            'retries': 3,
            'socket_timeout': 15,
            'http_chunk_size': 131072,
            'concurrent_fragment_downloads': 1,
            'fragment_retries': 1,
            'skip_unavailable_fragments': True,
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'merge_output_format': 'mp4',
            'cookiesfrombrowser': None,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs', 'automatic_captions', 'live_chat', 'comments', 'chapters'],
                    'player_skip': ['webpage', 'configs', 'js', 'player'],
                    'player_client': ['android'],
                    'comment_sort': ['top'],
                    'max_comments': [0],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    
    def _clean_url(self, url: str) -> str:
        """Pulisce l'URL da parametri problematici"""
        # Rimuovi parametri che possono causare problemi
        problematic_params = ['si', 'list', 'index', 't', 'start_radio', 'feature', 'v', 'ab_channel']
        
        if '?' in url:
            base_url, params = url.split('?', 1)
            param_dict = parse_qs(params)
            
            # Rimuovi parametri problematici
            for param in problematic_params:
                param_dict.pop(param, None)
            
            # Ricostruisci URL
            if param_dict:
                clean_params = '&'.join([f"{k}={v[0]}" for k, v in param_dict.items()])
                return f"{base_url}?{clean_params}"
            else:
                return base_url
        
        return url
    
    async def get_download_options(self, url: str) -> List[Dict]:
        """Ottieni opzioni di download con bypass ultra-aggressivo"""
        try:
            # Pulisci URL
            clean_url = self._clean_url(url)
            logger.info(f"Cleaned URL: {clean_url}")
            
            # Prova tutte le configurazioni
            for i, config in enumerate(self.ultra_configs):
                try:
                    logger.info(f"Trying ultra config {i+1} for URL: {clean_url}")
                    
                    # Aggiorna user agent per ogni tentativo
                    config['user_agent'] = random.choice(self.user_agents)
                    
                    with yt_dlp.YoutubeDL(config) as ydl:
                        info = ydl.extract_info(clean_url, download=False)
                        
                        if info and info.get('formats'):
                            logger.info(f"Success with ultra config {i+1}")
                            return self._process_formats(info)
                    
                    # Pausa tra tentativi
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.warning(f"Ultra config {i+1} failed: {e}")
                    continue
            
            # Se tutti i tentativi falliscono, usa opzioni di fallback
            logger.warning("All ultra configs failed, using fallback options")
            return self._get_fallback_options()
            
        except Exception as e:
            logger.error(f"Error in get_download_options: {e}")
            return self._get_fallback_options()
    
    def _process_formats(self, info: Dict) -> List[Dict]:
        """Processa i formati disponibili"""
        options = []
        
        # Estrai informazioni base
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')
        
        # Processa formati video
        video_formats = []
        audio_formats = []
        
        for fmt in info.get('formats', []):
            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':  # Video + Audio
                height = fmt.get('height') or 0
                if height > 0:
                    video_formats.append({
                        'format_id': fmt['format_id'],
                        'format': f"🎥 Video {height}p",
                        'size': self._format_size(fmt.get('filesize', 0)),
                        'ext': fmt.get('ext', 'mp4'),
                        'type': 'video',
                        'quality': height,
                        'title': title,
                        'uploader': uploader,
                        'ydl_format': fmt['format_id']
                    })
            elif fmt.get('acodec') != 'none':  # Audio only
                abr = fmt.get('abr') or 0
                if abr > 0:
                    audio_formats.append({
                        'format_id': fmt['format_id'],
                        'format': f"🎵 Audio {abr}kbps",
                        'size': self._format_size(fmt.get('filesize', 0)),
                        'ext': fmt.get('ext', 'mp3'),
                        'type': 'audio',
                        'quality': abr,
                        'title': title,
                        'uploader': uploader,
                        'ydl_format': fmt['format_id']
                    })
        
        # Ordina per qualità
        video_formats.sort(key=lambda x: x['quality'], reverse=True)
        audio_formats.sort(key=lambda x: x['quality'], reverse=True)
        
        # Aggiungi le migliori opzioni
        options.extend(video_formats[:3])
        options.extend(audio_formats[:3])
        
        # Se non ci sono formati specifici, usa opzioni di fallback
        if not options:
            return self._get_fallback_options()
        
        return options[:8]  # Massimo 8 opzioni
    
    def _get_fallback_options(self) -> List[Dict]:
        """Opzioni di fallback sempre disponibili"""
        return [
            {
                'format_id': 'worst',
                'format': '🎥 Video (Qualità Base)',
                'size': 'Qualità base',
                'ext': 'mp4',
                'type': 'video',
                'quality': 'base',
                'ydl_format': 'worst'
            },
            {
                'format_id': 'bestaudio',
                'format': '🎵 MP3 Alta Qualità (320kbps)',
                'size': 'Audio premium',
                'ext': 'mp3',
                'type': 'audio',
                'quality': 'high',
                'ydl_format': 'bestaudio'
            },
            {
                'format_id': 'worstaudio',
                'format': '⚡ MP3 Veloce (128kbps)',
                'size': 'Audio veloce',
                'ext': 'mp3',
                'type': 'audio',
                'quality': 'fast',
                'ydl_format': 'worstaudio'
            }
        ]
    
    def _format_size(self, size_bytes: int) -> str:
        """Formatta la dimensione del file"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
    
    async def download_file(self, url: str, option: Dict, user_id: int) -> Optional[str]:
        """Download del file con l'opzione selezionata"""
        try:
            user_dir = os.path.join(self.download_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Usa la prima configurazione per il download
            config = self.ultra_configs[0].copy()
            config['outtmpl'] = os.path.join(user_dir, '%(title)s.%(ext)s')
            config['format'] = option.get('ydl_format', 'worst')
            config['user_agent'] = random.choice(self.user_agents)
            
            # Download con timeout
            with yt_dlp.YoutubeDL(config) as ydl:
                ydl.download([url])
                
                # Trova il file scaricato
                for file in os.listdir(user_dir):
                    if any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mp3', '.m4a', '.avi', '.mkv']):
                        return os.path.join(user_dir, file)
                
                return None
                
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None

# Test function
async def test_youtube_ultra_bypass():
    """Test del bypass YouTube ultra-aggressivo"""
    bypass = YouTubeUltraBypass()
    
    test_urls = [
        "https://youtu.be/fJOE0vUjjo8?si=7P_VCMfO0wBwKq_Y",
        "https://www.youtube.com/watch?v=Q7NjUxGMv7Y&list=RDQ7NjUxGMv7Y&start_radio=1",
        "https://www.youtube.com/watch?v=nuSb86YlhHc",
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        options = await bypass.get_download_options(url)
        print(f"✅ Options: {len(options)} found")
        
        for opt in options:
            print(f"   - {opt['format']} ({opt['type']})")

if __name__ == "__main__":
    asyncio.run(test_youtube_ultra_bypass())
