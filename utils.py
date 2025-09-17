import re
from typing import Optional
from config import SUPPORTED_PLATFORMS, FILE_TYPES

def detect_platform(url: str) -> Optional[str]:
    """Detect platform from URL"""
    url_lower = url.lower()
    
    # Special handling for YouTube URLs with parameters
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower or 'music.youtube.com' in url_lower:
        return 'youtube'
    
    # First check known platforms
    for platform, domains in SUPPORTED_PLATFORMS.items():
        if any(domain in url_lower for domain in domains):
            return platform
    
    # If it's a valid URL but unknown platform, return 'generic'
    if is_valid_url(url):
        return 'generic'
    
    return None

def get_file_type(filename: str) -> str:
    """Get file type from filename"""
    if not filename:
        return 'unknown'
    
    ext = filename.lower().split('.')[-1]
    
    for file_type, extensions in FILE_TYPES.items():
        if f'.{ext}' in extensions:
            return file_type
    
    return 'unknown'

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    # More flexible URL pattern that handles parameters and fragments
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?].*)?$', re.IGNORECASE)  # Allow any path and parameters
    
    return url_pattern.match(url) is not None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename

def get_platform_icon(platform: str) -> str:
    """Get emoji icon for platform"""
    icons = {
        'youtube': '📺',
        'instagram': '📷',
        'tiktok': '🎵',
        'twitter': '🐦',
        'facebook': '👥',
        'reddit': '🔴',
        'vimeo': '🎬',
        'dailymotion': '🎥'
    }
    return icons.get(platform, '🔗')

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
