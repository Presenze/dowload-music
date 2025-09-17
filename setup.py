#!/usr/bin/env python3
"""
Setup script for Giglio Download Unlimited Bot
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            print("📝 Creating .env file from template...")
            with open('env_example.txt', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✅ .env file created! Please edit it with your bot token.")
        else:
            print("❌ env_example.txt not found!")
            return False
    else:
        print("ℹ️  .env file already exists")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    print("✅ Directories created!")

def main():
    """Main setup function"""
    print("🌸 Giglio Download Unlimited Bot Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your bot token")
    print("2. Run: python run.py")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main()
