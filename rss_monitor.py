#!/usr/bin/env python3
"""
Digital Dentistry RSS Monitor
Secure version with environment variable configuration
"""

import feedparser
import requests
import json
import time
import os
from datetime import datetime, timezone
from pathlib import Path

# Configuration paths
CONFIG_FILE = "rss_config.json"
LAST_CHECK_FILE = "last_check.json"

def load_config():
    """Load configuration from JSON file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"❌ Configuration file {CONFIG_FILE} not found!")
        return None

def load_last_check():
    """Load last check timestamps"""
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_last_check(last_check):
    """Save last check timestamps"""
    with open(LAST_CHECK_FILE, 'w', encoding='utf-8') as f:
        json.dump(last_check, f, indent=2)

def parse_datetime(date_string):
    """Parse various datetime formats to timezone-aware datetime"""
    if not date_string:
        return datetime.now(timezone.utc)
    
    # Try common RSS datetime formats
    formats = [
        '%Y-%m-%dT%H:%M:%SZ',
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%d %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_string, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    
    # If all parsing fails, return current time
    return datetime.now(timezone.utc)

def contains_keywords(text, keywords):
    """Check if text contains any of the keywords"""
    if not text:
        return False
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False

def send_telegram_message(message):
    """Send message via Telegram using environment variables"""
    import os
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in environment variables")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Telegram message failed: {e}")
        return False

def check_rss_sources(config, last_check):
    """Check all RSS sources for new articles"""
    new_articles = []
    current_time = datetime.now(timezone.utc)
    
    for source in config['rss_sources']:
        if not source.get('enabled', True):
            continue
            
        source_name = source['name']
        source_url = source['url']
        
        print(f"🔍 Checking {source_name}...")
        
        # Get last check time for this source
        last_check_time = last_check.get(source_name, "1970-01-01T00:00:00Z")
        last_check_dt = parse_datetime(last_check_time)
        
        # Fetch RSS feed
        try:
            feed = feedparser.parse(source_url)
            if not feed.entries:
                print(f"   ⚠️  No data for {source_name}")
                continue
        except Exception as e:
            print(f"   ❌ Error fetching {source_name}: {e}")
            continue
        
        # Check for new articles
        source_new_articles = []
        for entry in feed.entries:
            published = getattr(entry, 'published', getattr(entry, 'updated', ''))
            pub_dt = parse_datetime(published)
            
            # Check if article is newer than last check
            if pub_dt > last_check_dt:
                title = getattr(entry, 'title', '')
                summary = getattr(entry, 'summary', '')
                content = getattr(entry, 'content', [{}])[0].get('value', '') if entry.get('content') else ''
                
                full_text = f"{title} {summary} {content}"
                if contains_keywords(full_text, config['keywords']):
                    article = {
                        'source': source_name,
                        'title': title,
                        'link': entry.link,
                        'published': published,
                        'summary': summary[:200] + "..." if len(summary) > 200 else summary
                    }
                    source_new_articles.append(article)
        
        if source_new_articles:
            print(f"   ✅ Found {len(source_new_articles)} new articles")
            new_articles.extend(source_new_articles)
        else:
            print(f"   📭 No new articles")
        
        # Update last check time for this source
        last_check[source_name] = current_time.isoformat()
    
    return new_articles, last_check

def format_telegram_message(articles):
    """Format articles into Telegram message"""
    if not articles:
        return None
        
    message = "🦷 <b>Digital Dentistry News Update</b>\n\n"
    
    for article in articles[:10]:
        message += f"📰 <b>{article['source']}</b>\n"
        message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
        if article['summary']:
            message += f"📝 {article['summary']}\n"
        message += f"⏰ {article['published']}\n\n"
    
    if len(articles) > 10:
        message += f"... and {len(articles) - 10} more articles\n"
    
    return message

def main():
    """Main function"""
    print("🦷 Digital Dentistry RSS Monitor starting...")
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    print("✅ Configuration loaded successfully")
    
    # Check environment variables
    import os
    if not os.getenv('TELEGRAM_BOT_TOKEN') or not os.getenv('TELEGRAM_CHAT_ID'):
        print("❌ Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
        return
    
    print("✅ Environment variables configured securely")
    
    # Load last check times
    last_check = load_last_check()
    
    # Check RSS sources
    new_articles, updated_last_check = check_rss_sources(config, last_check)
    
    if new_articles:
        print(f"✅ Found {len(new_articles)} relevant articles")
        
        # Format and send Telegram message
        message = format_telegram_message(new_articles)
        if message:
            success = send_telegram_message(message)
            if success:
                print("✅ Telegram message sent successfully")
            else:
                print("❌ Failed to send Telegram message")
    else:
        print("📭 No new relevant articles found")
    
    # Save last check times
    save_last_check(updated_last_check)
    print("💾 Last check times saved")

if __name__ == "__main__":
    main()