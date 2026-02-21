#!/home/linuxbrew/.linuxbrew/bin/python3
"""
Digital Dentistry RSS Monitor
Monitors multiple RSS sources for digital dentistry content with AI summarization.
"""

import feedparser
import requests
import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Configuration
CONFIG_FILE = "rss_config.json"
LAST_CHECK_FILE = "last_check.json"

def load_config():
    """Load configuration from JSON file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"❌ Configuration file {CONFIG_FILE} not found!")
        sys.exit(1)

def get_env_config():
    """Get configuration from environment variables"""
    config = {}
    config['telegram_bot_token'] = os.environ.get('TELEGRAM_BOT_TOKEN')
    config['telegram_chat_id'] = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not config['telegram_bot_token'] or not config['telegram_chat_id']:
        print("❌ TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables required!")
        sys.exit(1)
    
    return config

def test_telegram_connection(bot_token, chat_id):
    """Test Telegram connection"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": "✅ Digital Dentistry Monitor: Configuration test successful!",
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Telegram connection failed: {e}")
        return False

def fetch_rss_feed(url):
    """Fetch RSS feed"""
    try:
        feed = feedparser.parse(url)
        return feed
    except Exception as e:
        print(f"⚠️  RSS fetch failed ({url}): {e}")
        return None

def parse_datetime(date_string):
    """Parse various datetime formats"""
    if not date_string:
        return datetime.now(timezone.utc)
    
    # Try common formats
    formats = [
        '%Y-%m-%dT%H:%M:%SZ',
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S%z'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    
    # If all fail, return current time
    return datetime.now(timezone.utc)

def contains_keywords(text, keywords):
    """Check if text contains any keywords"""
    if not text:
        return False
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False

def send_telegram_message(bot_token, chat_id, message):
    """Send Telegram message"""
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

def load_last_check():
    """Load last check times"""
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_last_check(last_check):
    """Save last check times"""
    with open(LAST_CHECK_FILE, 'w', encoding='utf-8') as f:
        json.dump(last_check, f, indent=2)

def generate_summary_and_priority(title, content, source):
    """Generate summary and priority (simplified version)"""
    # Simple priority logic based on source and keywords
    high_priority_sources = ['ADA News', 'Align Technology News', 'exocad Blog']
    high_priority_keywords = ['launch', 'new product', 'breakthrough', 'innovation', 'release']
    
    priority = 'medium'
    priority_emoji = '🟡'
    
    if source in high_priority_sources:
        priority = 'high'
        priority_emoji = '🔴'
    elif any(kw in content.lower() for kw in high_priority_keywords):
        priority = 'high'
        priority_emoji = '🔴'
    elif 'update' in content.lower() or 'news' in content.lower():
        priority = 'low'
        priority_emoji = '🟢'
    
    # Simple summary (first 200 characters)
    summary = content[:200] + "..." if len(content) > 200 else content
    
    return {
        'summary': summary,
        'priority': priority,
        'priority_emoji': priority_emoji
    }

def check_rss_sources(config, last_check):
    """Check all RSS sources"""
    new_articles = []
    current_time = datetime.now(timezone.utc)
    
    rss_config = load_config()
    keywords = rss_config.get('keywords', [])
    sources = rss_config.get('rss_sources', [])
    
    for source in sources:
        if not source.get('enabled', True):
            continue
            
        source_name = source['name']
        source_url = source['url']
        
        print(f"🔍 Checking {source_name}...")
        
        # Get last check time
        last_check_time = last_check.get(source_name, "1970-01-01T00:00:00Z")
        last_check_dt = parse_datetime(last_check_time)
        
        # Fetch RSS feed
        feed = fetch_rss_feed(source_url)
        if not feed or not feed.entries:
            print(f"   ⚠️  No data for {source_name}")
            continue
        
        # Check for new articles
        source_new_articles = []
        for entry in feed.entries:
            published = getattr(entry, 'published', getattr(entry, 'updated', ''))
            pub_dt = parse_datetime(published)
            
            # Check if article is new
            if pub_dt > last_check_dt:
                title = getattr(entry, 'title', '')
                summary = getattr(entry, 'summary', '')
                content = getattr(entry, 'content', [{}])[0].get('value', '') if entry.get('content') else ''
                
                full_text = f"{title} {summary} {content}"
                if contains_keywords(full_text, keywords):
                    summary_result = generate_summary_and_priority(title, full_text, source_name)
                    
                    article = {
                        'source': source_name,
                        'title': title,
                        'link': entry.link,
                        'published': published,
                        'summary': summary_result['summary'],
                        'priority': summary_result['priority'],
                        'priority_emoji': summary_result['priority_emoji']
                    }
                    source_new_articles.append(article)
        
        if source_new_articles:
            print(f"   ✅ Found {len(source_new_articles)} new articles")
            new_articles.extend(source_new_articles)
        else:
            print(f"   📭 No new articles")
        
        # Update last check time
        last_check[source_name] = current_time.isoformat()
    
    return new_articles, last_check

def format_telegram_message(articles):
    """Format Telegram message with priority grouping"""
    if not articles:
        return None
        
    # Group by priority
    high_priority = [a for a in articles if a['priority'] == 'high']
    medium_priority = [a for a in articles if a['priority'] == 'medium']
    low_priority = [a for a in articles if a['priority'] == 'low']
    
    message = "🦷 <b>Digital Dentistry Updates</b>\n\n"
    
    if high_priority:
        message += "🔴 <b>High Priority</b>\n"
        for article in high_priority[:5]:
            message += f"📰 {article['source']}\n"
            message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
            if article['summary']:
                message += f"📝 {article['summary']}\n"
            message += "\n"
    
    if medium_priority:
        message += "🟡 <b>Medium Priority</b>\n"
        for article in medium_priority[:5]:
            message += f"📰 {article['source']}\n"
            message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
            if article['summary']:
                message += f"📝 {article['summary']}\n"
            message += "\n"
    
    if low_priority:
        message += "🟢 <b>Low Priority</b>\n"
        for article in low_priority[:3]:
            message += f"📰 {article['source']}\n"
            message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
            if article['summary']:
                message += f"📝 {article['summary']}\n"
            message += "\n"
    
    return message.strip()

def main():
    """Main function"""
    print("🦷 Digital Dentistry RSS Monitor starting...")
    
    # Load configurations
    env_config = get_env_config()
    print("✅ Environment variables configured securely")
    
    # Test Telegram connection in test mode
    if '--test' in sys.argv:
        print("🧪 Testing Telegram connection...")
        if test_telegram_connection(env_config['telegram_bot_token'], env_config['telegram_chat_id']):
            print("✅ Telegram connection successful!")
        else:
            print("❌ Telegram connection failed!")
            sys.exit(1)
        return
    
    # Load RSS configuration
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Configuration file {CONFIG_FILE} not found!")
        sys.exit(1)
    print("✅ Configuration loaded successfully")
    
    # Load last check times
    last_check = load_last_check()
    
    # Check RSS sources
    new_articles, updated_last_check = check_rss_sources(env_config, last_check)
    
    if new_articles:
        print(f"✅ Found {len(new_articles)} relevant articles")
        message = format_telegram_message(new_articles)
        if message:
            if send_telegram_message(env_config['telegram_bot_token'], env_config['telegram_chat_id'], message):
                print("✅ Telegram message sent successfully!")
            else:
                print("❌ Failed to send Telegram message")
    else:
        print("📭 No new relevant articles found")
    
    # Save last check times
    save_last_check(updated_last_check)
    print("💾 Last check times saved")

if __name__ == "__main__":
    main()