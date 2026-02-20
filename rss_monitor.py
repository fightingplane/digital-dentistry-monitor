#!/usr/bin/env python3
"""
Digital Dentistry RSS Monitor with AI Summarization
Secure version using environment variables for sensitive data.
"""

import os
import json
import feedparser
import requests
from datetime import datetime

# Configuration
CONFIG_FILE = "rss_config.json"
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def load_config():
    """Load configuration from JSON file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def send_telegram_message(message):
    """Send message via Telegram bot"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Missing Telegram environment variables")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def main():
    """Main monitoring function"""
    print("🦷 Digital Dentistry RSS Monitor starting...")
    
    # Check environment variables
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Error: Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
        return
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Error: No configuration found")
        return
    
    print("✅ Configuration loaded successfully")
    print("✅ Environment variables configured securely")
    print("✅ Ready to monitor digital dentistry news!")

if __name__ == "__main__":
    main()