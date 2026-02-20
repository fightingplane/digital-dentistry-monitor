#!/bin/bash

# RSS Monitor Deployment Script
# Creates necessary directories and sets up the monitor

set -e

echo "🚀 Setting up Dental Digital RSS Monitor..."

# Create directories
mkdir -p /home/admin/.openclaw/workspace/dental-digital-monitor/data
mkdir -p /home/admin/.openclaw/workspace/dental-digital-monitor/logs

# Install required Python packages
pip3 install feedparser requests pyyaml python-telegram-bot beautifulsoup4 lxml

# Make script executable
chmod +x /home/admin/.openclaw/workspace/dental-digital-monitor/rss_monitor.py

echo "✅ Setup complete!"
echo "📋 To run manually: python3 rss_monitor.py"
echo "⏰ To schedule automatic checks, add to crontab:"
echo "0 */6 * * * cd /home/admin/.openclaw/workspace/dental-digital-monitor && python3 rss_monitor.py >> logs/rss_monitor.log 2>&1"