#!/usr/bin/env python3
import json

# 读取配置文件并测试结构
with open('rss_config.json', 'r') as f:
    config = json.load(f)

print("配置文件结构:")
print(f"Telegram bot_token: {config['telegram']['bot_token'][:20]}...")
print(f"Telegram chat_id: {config['telegram']['chat_id']}")
print(f"RSS 源数量: {len(config['rss_sources'])}")

# 测试第一个 RSS 源
first_source = config['rss_sources'][0]
print(f"第一个源: {first_source['name']} - {first_source['url']}")