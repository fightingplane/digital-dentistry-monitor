#!/bin/bash

# Deploy script for Digital Dentistry RSS Monitor
# Sets up environment variables and starts the monitoring service

set -e

echo "🚀 Deploying Digital Dentistry RSS Monitor..."

# Check if required environment variables are set
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "❌ Error: Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables"
    echo "   export TELEGRAM_BOT_TOKEN='your_bot_token'"
    echo "   export TELEGRAM_CHAT_ID='your_chat_id'"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install feedparser requests python-telegram-bot pyyaml beautifulsoup4 lxml

# Test the configuration
echo "🧪 Testing configuration..."
python rss_monitor.py --test

# Start the monitoring service (in production, you'd use systemd or cron)
echo "✅ Deployment complete!"
echo "💡 To run manually: python rss_monitor.py"
echo "⏰ To schedule automatic checks, add to crontab:"
echo "   0 */6 * * * cd /path/to/digital-dentistry-monitor && python rss_monitor.py >> logs/monitor.log 2>&1"