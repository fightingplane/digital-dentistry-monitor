#!/bin/bash

# Deploy script for Digital Dentistry RSS Monitor
# Sets up environment variables and starts the monitoring service

set -e

# Get the current directory automatically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Deploying Digital Dentistry RSS Monitor..."
echo "📁 Working directory: $SCRIPT_DIR"

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
python "$SCRIPT_DIR/rss_monitor.py" --test

# Start the monitoring service (in production, you'd use systemd or cron)
echo "✅ Deployment complete!"
echo "💡 To run manually: cd $SCRIPT_DIR && python rss_monitor.py"
echo "⏰ To schedule automatic checks, add to crontab:"
echo "   0 */6 * * * cd $SCRIPT_DIR && python rss_monitor.py >> $SCRIPT_DIR/logs/monitor.log 2>&1"