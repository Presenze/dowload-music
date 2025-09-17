#!/usr/bin/env python3
"""
Test script for Giglio Download Bot
"""

import asyncio
from downloader import DownloadManager

async def test_download_options():
    """Test download options for different platforms"""
    downloader = DownloadManager()
    
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - GANGNAM STYLE
    ]
    
    for url in test_urls:
        print(f"\n🔗 Testing URL: {url}")
        try:
            options = await downloader.get_download_options(url, "youtube")
            print(f"✅ Found {len(options)} options:")
            for i, option in enumerate(options):
                print(f"  {i+1}. {option['format']} - {option['size']}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Giglio Download Bot...")
    asyncio.run(test_download_options())
