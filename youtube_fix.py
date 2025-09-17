#!/usr/bin/env python3
"""
YouTube Fix - Alternative downloader for YouTube videos
This bypasses YouTube authentication by using different methods
"""

import os
import re
import asyncio
import logging
from typing import List, Dict, Optional
import yt_dlp

logger = logging.getLogger(__name__)

class YouTubeFix:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Alternative YouTube configuration that bypasses auth
        self.ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'worst',  # Use worst quality to avoid auth
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 0,  # No retries
            'fragment_retries': 0,   # No retries
            'retries': 0,            # No retries
            'socket_timeout': 30,    # Longer timeout
            'http_chunk_size': 1048576,  # 1MB chunks
            'concurrent_fragment_downloads': 1,  # Single download
            'skip_unavailable_fragments': True,
            # YouTube bypass settings
            'cookiesfrombrowser': None,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs', 'automatic_captions'],
                    'player_skip': ['webpage', 'configs'],
                    'player_client': ['android_music'],  # Use music client
                }
            },
            # Additional bypass settings
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'com.google.android.music/5.10.31 (Linux; U; Android 10; SM-G973F Build/QP1A.190711.020)',
        }
    
    async def get_download_options(self, url: str) -> List[Dict]:
        """Get download options for YouTube URL"""
        try:
            # Clean URL
            if '&list=' in url:
                url = url.split('&list=')[0]
            if '&start_radio=' in url:
                url = url.split('&start_radio=')[0]
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return self._get_fallback_options()
                
                # Extract basic info
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                
                # Return simple options
                options = [
                    {
                        'format_id': 'worst',
                        'format': '🎵 Audio/Video (Qualità Base)',
                        'size': f'{duration//60}min' if duration else 'Unknown',
                        'ext': 'mp4',
                        'type': 'video',
                        'title': title
                    }
                ]
                
                return options
                
        except Exception as e:
            logger.error(f"YouTube fix error: {e}")
            return self._get_fallback_options()
    
    def _get_fallback_options(self) -> List[Dict]:
        """Return fallback options when extraction fails"""
        return [
            {
                'format_id': 'worst',
                'format': '🎵 Download Base (Senza Auth)',
                'size': 'Qualità base',
                'ext': 'mp4',
                'type': 'video'
            }
        ]
    
    async def download_video(self, url: str, user_id: int) -> Optional[str]:
        """Download YouTube video with bypass"""
        try:
            user_dir = os.path.join(self.download_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Update output template for user directory
            opts = self.ydl_opts.copy()
            opts['outtmpl'] = os.path.join(user_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Download the video
                ydl.download([url])
                
                # Find the downloaded file
                for file in os.listdir(user_dir):
                    if any(file.endswith(ext) for ext in ['.mp4', '.webm', '.m4a', '.mp3']):
                        return os.path.join(user_dir, file)
                
                return None
                
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None

# Test function
async def test_youtube_fix():
    """Test the YouTube fix"""
    fix = YouTubeFix()
    
    # Test URLs
    test_urls = [
        "https://youtu.be/fJOE0vUjjo8?si=7P_VCMfO0wBwKq_Y",
        "https://www.youtube.com/watch?v=Q7NjUxGMv7Y&list=RDQ7NjUxGMv7Y&start_radio=1"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        options = await fix.get_download_options(url)
        print(f"✅ Options: {len(options)} found")
        for opt in options:
            print(f"   - {opt['format']}")

if __name__ == "__main__":
    asyncio.run(test_youtube_fix())
