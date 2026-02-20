# Dental Digital RSS Monitor

Automated RSS monitoring system for digital dentistry news and updates with AI-powered summarization and priority classification.

## Features
- 🦷 Monitors 10+ RSS sources for digital dentistry content
- 🔍 Intelligent keyword filtering (English & Chinese)
- 📊 AI-powered content summarization and priority classification
- 🔴🟡🟢 Priority levels: High, Medium, Low importance
- 🔒 Secure configuration using environment variables
- 🤖 Telegram notifications with clickable links
- ⏰ Configurable check intervals

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/fightingplane/digital-dentistry-monitor.git
cd digital-dentistry-monitor
```

### 2. Install Dependencies
```bash
pip install feedparser requests python-telegram-bot pyyaml beautifulsoup4 lxml
```

### 3. Configure Environment Variables
```bash
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHAT_ID="your_telegram_chat_id"
```

### 4. Customize Configuration (Optional)
Edit `rss_config.json` to:
- Add/remove RSS sources
- Modify keywords
- Adjust check intervals

### 5. Run the Monitor
```bash
python rss_monitor.py
```

## Files
- `rss_monitor.py` - Main monitoring script
- `deploy.sh` - Deployment and setup script  
- `rss_config.json` - Configuration file (safe, no sensitive data)
- `.gitignore` - Prevents accidental commits of sensitive files

## Security
- Sensitive data (bot token, chat ID) stored only in environment variables
- Configuration file contains only non-sensitive settings
- .gitignore prevents accidental exposure of credentials

## License
MIT License