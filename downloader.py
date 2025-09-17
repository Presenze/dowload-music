import os
import asyncio
import yt_dlp
import aiohttp
import logging
from typing import List, Dict, Optional
from config import SUPPORTED_PLATFORMS, DOWNLOAD_DIR

logger = logging.getLogger(__name__)

class DownloadManager:
    def __init__(self):
        self.download_dir = DOWNLOAD_DIR
        os.makedirs(self.download_dir, exist_ok=True)
        
        # yt-dlp configuration - VELOCITÀ MASSIMA + QUALITÀ + RAILWAY COMPATIBLE
        self.ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'format': 'worst[height<=480]/worst',  # Use worst quality to avoid auth
            'noplaylist': True,
            'extract_flat': False,
            'no_warnings': True,
            'ignoreerrors': True,
            'writethumbnail': False,
            'writeinfojson': False,
            'extractor_retries': 1,
            'fragment_retries': 1,
            'retries': 1,
            'socket_timeout': 15,  # Timeout aumentato per Railway
            'http_chunk_size': 1048576,  # Chunk 1MB per Railway
            'concurrent_fragment_downloads': 2,  # Ridotto per Railway
            'fragment_retries': 1,  # 1 retry per stabilità
            'skip_unavailable_fragments': True,
            # Railway specific settings
            'prefer_insecure': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
            # FFmpeg settings for Railway
            'ffmpeg_location': '/usr/bin/ffmpeg',  # Railway FFmpeg path
            'merge_output_format': 'mp4',  # Force MP4 output
            # YouTube authentication bypass
            'cookiesfrombrowser': None,  # Disable cookies
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls', 'translated_subs'],  # Skip problematic formats
                    'player_skip': ['webpage'],
                    'player_client': ['android'],  # Only mobile client
                }
            },
        }
    
    async def get_download_options(self, url: str, platform: str) -> List[Dict]:
        """Get available download options for a URL"""
        try:
            # Special handling for YouTube Music links
            if 'music.youtube.com' in url:
                url = url.replace('music.youtube.com', 'www.youtube.com')
            
            # For generic URLs, try to download directly first
            if platform == 'generic':
                return await self.get_generic_download_options(url)
            
            # YouTube specific handling - Use alternative method
            if 'youtube.com' in url or 'youtu.be' in url:
                # Use YouTube fix for better bypass
                from youtube_fix import YouTubeFix
                youtube_fix = YouTubeFix()
                return await youtube_fix.get_download_options(url)
            else:
                opts = self.ydl_opts.copy()
                opts['extract_flat'] = False
                opts['no_warnings'] = True
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return []
                
                options = []
                
                # Video options
                if 'formats' in info:
                    # Collect all formats first
                    video_formats = []
                    audio_formats = []
                    
                    for fmt in info['formats']:
                        if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':  # Video + Audio
                            height = fmt.get('height') or 0
                            video_formats.append({
                                'format_id': fmt['format_id'],
                                'format': f"🎥 Video {height if height > 0 else 'Unknown'}p",
                                'size': self._format_size(fmt.get('filesize', 0)),
                                'ext': fmt.get('ext', 'mp4'),
                                'type': 'video',
                                'quality': height
                            })
                        elif fmt.get('vcodec') != 'none':  # Video only
                            height = fmt.get('height') or 0
                            video_formats.append({
                                'format_id': fmt['format_id'],
                                'format': f"🎬 Video {height if height > 0 else 'Unknown'}p (no audio)",
                                'size': self._format_size(fmt.get('filesize', 0)),
                                'ext': fmt.get('ext', 'mp4'),
                                'type': 'video_only',
                                'quality': height
                            })
                        elif fmt.get('acodec') != 'none':  # Audio only
                            abr = fmt.get('abr') or 0
                            audio_formats.append({
                                'format_id': fmt['format_id'],
                                'format': f"🎵 Audio {abr if abr > 0 else 'Unknown'}kbps",
                                'size': self._format_size(fmt.get('filesize', 0)),
                                'ext': fmt.get('ext', 'mp3'),
                                'type': 'audio',
                                'quality': abr
                            })
                    
                    # Sort by quality (highest first) - gestisci None values
                    video_formats.sort(key=lambda x: x['quality'] or 0, reverse=True)
                    audio_formats.sort(key=lambda x: x['quality'] or 0, reverse=True)
                    
                    # Add best options first
                    options.extend(video_formats[:5])  # Top 5 video formats
                    options.extend(audio_formats[:3])  # Top 3 audio formats
                
                # If no formats found, add default options - VIDEO CON AUDIO + MP3 QUALITÀ
                if not options:
                    options.extend([
                        {
                            'format_id': 'best[height<=720]+bestaudio',
                            'format': '🎬 Video HD + Audio (720p)',
                            'size': 'Alta qualità',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'best[height<=480]+bestaudio',
                            'format': '🎥 Video + Audio (480p)',
                            'size': 'Media qualità',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'best[height<=360]+bestaudio',
                            'format': '⚡ Video + Audio (360p)',
                            'size': 'Veloce',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'bestaudio',
                            'format': '🎵 MP3 Alta Qualità (320kbps)',
                            'size': 'Audio premium',
                            'ext': 'mp3',
                            'type': 'audio'
                        },
                        {
                            'format_id': 'bestaudio[abr<=192]',
                            'format': '🎵 MP3 Qualità (192kbps)',
                            'size': 'Audio buono',
                            'ext': 'mp3',
                            'type': 'audio'
                        },
                        {
                            'format_id': 'worstaudio',
                            'format': '⚡ MP3 Veloce (128kbps)',
                            'size': 'Audio veloce',
                            'ext': 'mp3',
                            'type': 'audio'
                        }
                    ])
                
                # Add more default options if we have few - ULTRA VELOCI
                if len(options) < 6:
                    options.extend([
                        {
                            'format_id': 'worst[height<=240]',
                            'format': '⚡⚡ Video Ultra Veloce (240p)',
                            'size': 'Piccolissimo',
                            'ext': 'mp4',
                            'type': 'video'
                        },
                        {
                            'format_id': 'worstaudio[ext=m4a]',
                            'format': '⚡ Audio Veloce (M4A)',
                            'size': 'Piccolo',
                            'ext': 'm4a',
                            'type': 'audio'
                        },
                        {
                            'format_id': 'bestaudio[ext=m4a]',
                            'format': '🎵 Audio Qualità (M4A)',
                            'size': 'Medio',
                            'ext': 'm4a',
                            'type': 'audio'
                        }
                    ])
                
                return options[:12]  # Show up to 12 options
                
        except Exception as e:
            logger.error(f"Error getting download options: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Special handling for YouTube authentication errors
            if 'Sign in to confirm' in str(e) or 'cookies' in str(e).lower():
                logger.info("YouTube authentication required, trying alternative method...")
                # Try with different YouTube client
                try:
                    alt_opts = self.ydl_opts.copy()
                    alt_opts.update({
                        'extract_flat': False,
                        'no_warnings': True,
                        'format': 'worst',  # Use worst quality to avoid auth
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android'],  # Only mobile client
                                'skip': ['dash', 'hls', 'translated_subs'],
                            }
                        },
                    })
                    
                    with yt_dlp.YoutubeDL(alt_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        if info:
                            return [{
                                'format_id': 'worst',
                                'format': '🎵 Audio/Video (Qualità Base)',
                                'size': 'Qualità base',
                                'ext': 'mp4',
                                'type': 'video'
                            }]
                except:
                    pass
            
            # Return default options on error
            return [
                {
                    'format_id': 'best[height<=720]+bestaudio',
                    'format': '🎬 Video HD + Audio (720p)',
                    'size': 'Alta qualità',
                    'ext': 'mp4',
                    'type': 'video'
                },
                {
                    'format_id': 'best[height<=480]+bestaudio',
                    'format': '🎥 Video + Audio (480p)',
                    'size': 'Media qualità',
                    'ext': 'mp4',
                    'type': 'video'
                },
                {
                    'format_id': 'bestaudio',
                    'format': '🎵 MP3 Alta Qualità (320kbps)',
                    'size': 'Audio premium',
                    'ext': 'mp3',
                    'type': 'audio'
                },
                {
                    'format_id': 'worstaudio',
                    'format': '⚡ MP3 Veloce (128kbps)',
                    'size': 'Audio veloce',
                    'ext': 'mp3',
                    'type': 'audio'
                }
            ]
    
    async def download_file(self, url: str, option: Dict, user_id: int) -> Optional[str]:
        """Download file with selected option"""
        try:
            # Create user-specific directory
            user_dir = os.path.join(self.download_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Configure yt-dlp options
            ydl_opts = self.ydl_opts.copy()
            ydl_opts['outtmpl'] = os.path.join(user_dir, '%(title)s.%(ext)s')
            
            if option['type'] == 'direct':
                # Direct download without yt-dlp
                return await self.download_from_url(url, user_id)
            elif option['type'] == 'video_only':
                ydl_opts['format'] = f"{option['format_id']}+bestaudio"
            elif option['type'] == 'audio':
                ydl_opts['format'] = option['format_id']
                # Configure audio extraction - QUALITÀ MASSIMA
                if 'mp3' in option['ext'] or 'bestaudio' in option['format_id']:
                    if '320kbps' in option['format'] or 'Alta Qualità' in option['format']:
                        quality = '320'
                    elif '192kbps' in option['format'] or 'Qualità' in option['format']:
                        quality = '192'
                    else:
                        quality = '128'
                    
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }]
                elif 'm4a' in option['ext']:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                    }]
            else:
                ydl_opts['format'] = option['format_id']
            
            # Download with timeout protection - VELOCITÀ MASSIMA
            try:
                import asyncio
                
                # Set timeout for download
                async def download_with_timeout():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        return info
                
                # 30 second timeout
                info = await asyncio.wait_for(download_with_timeout(), timeout=30.0)
                
                if info:
                    # Find the downloaded file
                    for file in os.listdir(user_dir):
                        if file.endswith(option['ext']) or file.endswith('.webm') or file.endswith('.mp4'):
                            return os.path.join(user_dir, file)
                
                return None
            except asyncio.TimeoutError:
                logger.error("Download timeout - trying fallback")
                # Try to find any downloaded file as fallback
                for file in os.listdir(user_dir):
                    if any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mp3', '.m4a']):
                        return os.path.join(user_dir, file)
                return None
            except Exception as download_error:
                logger.error(f"Download failed: {download_error}")
                # Try to find any downloaded file as fallback
                for file in os.listdir(user_dir):
                    if any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mp3', '.m4a']):
                        return os.path.join(user_dir, file)
                return None
            
        except Exception as e:
            logger.error(f"Download error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    async def download_from_url(self, url: str, user_id: int) -> Optional[str]:
        """Download file directly from URL (for non-video platforms)"""
        try:
            user_dir = os.path.join(self.download_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Get filename from URL or content-disposition
                        filename = self._get_filename_from_url(url, response.headers)
                        file_path = os.path.join(user_dir, filename)
                        
                        with open(file_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                        
                        return file_path
            
            return None
            
        except Exception as e:
            logger.error(f"URL download error: {e}")
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes is None or size_bytes == 0:
            return "Unknown size"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def _get_filename_from_url(self, url: str, headers: Dict) -> str:
        """Extract filename from URL or headers"""
        # Try content-disposition header first
        if 'content-disposition' in headers:
            content_disp = headers['content-disposition']
            if 'filename=' in content_disp:
                filename = content_disp.split('filename=')[1].strip('"')
                return filename
        
        # Extract from URL
        filename = url.split('/')[-1].split('?')[0]
        if not filename or '.' not in filename:
            filename = f"download_{hash(url)}.bin"
        
        return filename
    
    async def get_generic_download_options(self, url: str) -> List[Dict]:
        """Get download options for generic URLs"""
        try:
            # Try to extract info with yt-dlp first
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info:
                    options = []
                    
                    # Check if it's a video/audio content
                    if 'formats' in info:
                        # Process formats like YouTube
                        video_formats = []
                        audio_formats = []
                        
                        for fmt in info['formats']:
                            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':  # Video + Audio
                                height = fmt.get('height') or 0
                                video_formats.append({
                                    'format_id': fmt['format_id'],
                                    'format': f"🎥 Video {height if height > 0 else 'Unknown'}p",
                                    'size': self._format_size(fmt.get('filesize', 0)),
                                    'ext': fmt.get('ext', 'mp4'),
                                    'type': 'video',
                                    'quality': height
                                })
                            elif fmt.get('acodec') != 'none':  # Audio only
                                abr = fmt.get('abr') or 0
                                audio_formats.append({
                                    'format_id': fmt['format_id'],
                                    'format': f"🎵 Audio {abr if abr > 0 else 'Unknown'}kbps",
                                    'size': self._format_size(fmt.get('filesize', 0)),
                                    'ext': fmt.get('ext', 'mp3'),
                                    'type': 'audio',
                                    'quality': abr
                                })
                        
                        # Sort by quality
                        video_formats.sort(key=lambda x: x['quality'] if x['quality'] is not None else 0, reverse=True)
                        audio_formats.sort(key=lambda x: x['quality'] if x['quality'] is not None else 0, reverse=True)
                        
                        options.extend(video_formats[:5])
                        options.extend(audio_formats[:3])
                    
                    if options:
                        return options[:12]
                
                # If yt-dlp can't handle it, try direct download
                return [{
                    'format_id': 'direct',
                    'format': '🔗 Download Diretto',
                    'size': 'Sconosciuto',
                    'ext': 'bin',
                    'type': 'direct',
                    'quality': 0
                }]
                
        except Exception as e:
            logger.error(f"Error with generic URL: {e}")
            # Fallback to direct download
            return [{
                'format_id': 'direct',
                'format': '🔗 Download Diretto',
                'size': 'Sconosciuto',
                'ext': 'bin',
                'type': 'direct',
                'quality': 0
            }]
