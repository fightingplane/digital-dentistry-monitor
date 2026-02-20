#!/usr/bin/env python3
"""
修复配置文件格式，将嵌套结构转换为扁平结构
"""

import json

# 读取当前配置
with open('rss_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 转换为扁平结构
flat_config = {
    'telegram_bot_token': config['telegram']['bot_token'],
    'telegram_chat_id': config['telegram']['chat_id'],
    'check_interval_hours': config['check_interval_hours'],
    'max_articles_per_check': config['max_articles_per_check'],
    'enable_summary': config['enable_summary'],
    'enable_priority_filtering': config['enable_priority_filtering'],
    'keywords': config['keywords'],
    'rss_sources': config['rss_sources']
}

# 保存为新配置文件
with open('rss_config_flat.json', 'w', encoding='utf-8') as f:
    json.dump(flat_config, f, indent=2, ensure_ascii=False)

print("✅ 配置文件格式已修复")
print(f"Telegram Token: {flat_config['telegram_bot_token'][:10]}...")
print(f"Chat ID: {flat_config['telegram_chat_id']}")
print(f"RSS 源数量: {len(flat_config['rss_sources'])}")