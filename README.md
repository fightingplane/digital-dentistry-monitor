# Dental Digital RSS Monitor

Automated RSS monitoring system for digital dentistry news and updates.

## Features
- Monitors multiple RSS sources for digital dentistry content
- Filters articles by relevant keywords
- Sends Telegram notifications for new relevant articles
- Configurable check interval and sources

## Setup
1. Clone this repository
2. Install dependencies: `pip install feedparser requests python-telegram-bot pyyaml beautifulsoup4 lxml`
3. Configure `rss_config.json` with your Telegram bot token and chat ID
4. Run `python rss_monitor.py` or set up as a cron job

## Configuration
Edit `rss_config.json` to customize:
- Telegram bot token and chat ID
- RSS sources to monitor
- Keywords for filtering
- Check interval

## Sources
Currently monitors:
- Dental Economics
- Dentistry Today  
- ADA News
- PubMed (digital dentistry research)

## License
MIT License