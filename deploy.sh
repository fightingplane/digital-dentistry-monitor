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

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Install dependencies
echo "📦 Installing dependencies..."
pip install feedparser requests python-telegram-bot pyyaml beautifulsoup4 lxml

# Test the configuration
echo "🧪 Testing configuration..."
python "$SCRIPT_DIR/rss_monitor.py" --test

# Setup crontab (every 6 hours)
PYTHON_PATH="$(which python)"
CRON_JOB="0 */6 * * * TELEGRAM_BOT_TOKEN='$TELEGRAM_BOT_TOKEN' TELEGRAM_CHAT_ID='$TELEGRAM_CHAT_ID' $PYTHON_PATH $SCRIPT_DIR/rss_monitor.py >> $SCRIPT_DIR/logs/monitor.log 2>&1"

# Check if cron job already exists, avoid duplicates
EXISTING_CRON=$(crontab -l 2>/dev/null || true)
if echo "$EXISTING_CRON" | grep -qF "rss_monitor.py"; then
    echo "⏰ Updating existing crontab entry..."
    # Remove old entry and add new one
    echo "$EXISTING_CRON" | grep -vF "rss_monitor.py" | { cat; echo "$CRON_JOB"; } | crontab -
else
    echo "⏰ Adding new crontab entry..."
    { echo "$EXISTING_CRON"; echo "$CRON_JOB"; } | crontab -
fi

echo "✅ Deployment complete!"
echo "💡 To run manually: cd $SCRIPT_DIR && python rss_monitor.py"
echo "⏰ Crontab configured: every 6 hours"
echo "📋 Current crontab:"
crontab -l