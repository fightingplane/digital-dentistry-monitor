# Dental Digital RSS Monitor

A specialized RSS monitoring system for tracking the latest trends and developments in digital dentistry.

## 🦷 Overview

This tool automatically monitors multiple RSS feeds from leading dental industry sources, filters content based on relevant keywords, and sends notifications via Telegram. It's designed specifically for dental professionals who want to stay updated with the latest advancements in digital dentistry technologies.

## 🎯 Features

- **Multi-source RSS Monitoring**: Track multiple dental industry news sources simultaneously
- **Smart Keyword Filtering**: Only receive updates relevant to digital dentistry
- **Telegram Integration**: Get instant notifications on your Telegram
- **Automated Scheduling**: Runs automatically every 6 hours
- **Duplicate Prevention**: Avoid receiving the same article multiple times
- **Easy Configuration**: Simple JSON configuration file for customization

## 🔍 Monitored Sources

- **Dental Economics** - Leading dental industry news and business insights
- **Dentistry Today** - Latest dental technology and clinical updates  
- **ADA News** - Official news from the American Dental Association
- **PubMed** - Academic research papers on digital dentistry

## 📋 Keywords Tracked

The system filters articles containing keywords such as:
- `digital dentistry`, `digital dental`
- `intraoral scanner`, `CAD/CAM`
- `3D printing dental`, `dental 3D printing`
- `AI dentistry`, `artificial intelligence dental`
- `dental software`, `dental technology`
- `dental innovation`

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Git
- Telegram Bot Token (from @BotFather)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/fightingplane/digital-dentistry-monitor.git
   cd digital-dentistry-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install feedparser requests python-telegram-bot pyyaml beautifulsoup4 lxml
   ```

3. **Configure Telegram**
   - Create a bot using [@BotFather](https://t.me/BotFather) on Telegram
   - Get your Bot Token and Chat ID
   - Update `rss_config.json` with your credentials

4. **Customize configuration** (optional)
   - Edit `rss_config.json` to add/remove RSS sources
   - Modify keywords in the configuration file
   - Adjust check interval frequency

5. **Run the monitor**
   ```bash
   python rss_monitor.py
   ```

## 🕐 Automated Scheduling

To run the monitor automatically every 6 hours, add this to your crontab:

```bash
0 */6 * * * cd /path/to/digital-dentistry-monitor && python rss_monitor.py >> logs/rss_monitor.log 2>&1
```

## 📁 Project Structure

```
digital-dentistry-monitor/
├── rss_monitor.py          # Main monitoring script
├── rss_config.json         # Configuration file
├── simple_monitor.py       # Simplified version for testing
├── deploy.sh               # Deployment script
├── README.md               # This file
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions workflow
```

## 🔒 Security Notes

- **Never commit your Telegram Bot Token** to version control
- Use environment variables or secure configuration files
- The default `rss_config.json` contains placeholder values for security

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add new RSS sources for digital dentistry
- Improve keyword filtering logic
- Enhance Telegram message formatting
- Add support for additional notification channels

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please open an issue on the GitHub repository.

---

**Built with ❤️ for the dental community**