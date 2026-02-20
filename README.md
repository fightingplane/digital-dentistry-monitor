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
Currently monitors the following sources:

### International Professional Media
- **Dental Economics** - Leading dental industry news
- **Dentistry Today** - Comprehensive dental technology coverage
- **Dental Tribune International** - Global dental news network
- **The Probe** - UK's leading dental magazine
- **Dental Product Shopper** - Product reviews and comparisons
- **Dental Lab Products** - Dental laboratory technology

### Technology Companies
- **ADA News** - American Dental Association official news
- **Align Technology Blog** - Invisalign and digital orthodontics
- **3Shape Blog** - Intraoral scanning and CAD/CAM solutions
- **exocad News** - Dental CAD software innovations
- **Envista Dental** - Nobel Biocare, KaVo, and digital implant solutions

### Academic & Research
- **PubMed** - Medical research (filtered for digital dentistry)
- **Journal of Digital Dentistry** - Peer-reviewed research
- **International Journal of Computerized Dentistry** - Technical research

### Chinese Sources
- **Chinese Stomatological Association** - Official academic organization
- **Today's Dentistry** - Chinese dental media
- **Dental Pioneer** - Digital dentistry technology in China

### Events & Conferences
- **IDS Cologne** - International Dental Show
- **Chicago Midwinter Meeting** - Major US dental conference
- **AAO Annual Session** - American Association of Orthodontists

## Keywords
The system filters articles containing these keywords:
- `digital dentistry`, `digital dental`, `intraoral scanner`
- `CAD/CAM`, `3D printing dental`, `dental 3D printing`
- `AI dentistry`, `artificial intelligence dental`
- `dental software`, `dental technology`, `dental innovation`
- `implant planning`, `digital workflow`, `virtual articulator`

## License
MIT License