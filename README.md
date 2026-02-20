# Dental Digital RSS Monitor

Automated RSS monitoring system for digital dentistry news and updates with AI-powered summarization.

## Features
- 🔍 Monitors 10+ RSS sources for digital dentistry content
- 🤖 AI-powered content summarization in Chinese
- 📊 Priority classification (High/Medium/Low importance)
- 🔒 Secure configuration using environment variables
- 📱 Telegram notifications with clickable links
- 🌐 Multi-language support (English & Chinese)

## Sources Monitored
- **International**: Dental Economics, Dentistry Today, Dental Tribune International, The Probe
- **Companies**: Align Technology, exocad, Envista Companies  
- **Academic**: PubMed, Journal of Digital Dentistry
- **Chinese**: 中华口腔医学会, 今日口腔

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
export TELEGRAM_CHAT_ID="your_chat_id"
```

### 4. Run the Monitor
```bash
python rss_monitor.py
```

### 5. Automated Scheduling (Optional)
Add to crontab for automatic checks every 6 hours:
```bash
0 */6 * * * cd /path/to/digital-dentistry-monitor && python rss_monitor.py >> logs/rss_monitor.log 2>&1
```

## Configuration
Edit `rss_config.json` to customize:
- RSS sources to monitor
- Keywords for filtering relevant content
- Check interval and article limits

## Security
- **Never commit sensitive data** - Use environment variables for Telegram credentials
- `.gitignore` prevents accidental commits of sensitive files
- All configuration files in repository are safe to share

## License
MIT License