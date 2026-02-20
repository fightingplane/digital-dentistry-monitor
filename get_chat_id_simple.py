#!/usr/bin/env python3
"""
Simple script to get Telegram chat ID using requests
"""
import requests
import json
import os

# Read config
with open('rss_config.json', 'r') as f:
    config = json.load(f)

bot_token = config['telegram']['bot_token']

# Get updates from Telegram
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data['ok'] and data['result']:
        # Get the most recent chat ID
        latest_update = data['result'][-1]
        if 'message' in latest_update:
            chat_id = latest_update['message']['chat']['id']
            chat_type = latest_update['message']['chat']['type']
            chat_title = latest_update['message']['chat'].get('title', 'Private Chat')
            
            print(f"✅ Found Chat ID: {chat_id}")
            print(f"   Type: {chat_type}")
            print(f"   Title/Name: {chat_title}")
            
            # Update config file
            config['telegram']['chat_id'] = str(chat_id)
            with open('rss_config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"✅ Config updated with Chat ID: {chat_id}")
        else:
            print("❌ No messages found. Please send a message to your bot first.")
    else:
        print("❌ No updates found. Please send a message to your bot first.")
else:
    print(f"❌ Error getting updates: {response.status_code}")
    print(response.text)