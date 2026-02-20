#!/usr/bin/env python3
"""
齿科数字化资讯 RSS 监控脚本
自动监控多个 RSS 源，过滤关键词，并通过 Telegram 发送通知
"""

import feedparser
import requests
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

# 配置文件路径
CONFIG_FILE = "rss_config.json"
LAST_CHECK_FILE = "last_check.json"

# 默认配置
DEFAULT_CONFIG = {
    "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
    "check_interval_hours": 1,
    "keywords": [
        "digital dentistry", "digital dental", "intraoral scanner", 
        "CAD/CAM", "3D printing dental", "dental 3D printing",
        "AI dentistry", "artificial intelligence dental",
        "dental software", "dental technology", "dental innovation"
    ],
    "rss_sources": [
        {
            "name": "Dental Economics",
            "url": "https://www.dentaleconomics.com/rss",
            "enabled": True
        },
        {
            "name": "Dentistry Today",
            "url": "https://www.dentistrytoday.com/feed/",
            "enabled": True
        },
        {
            "name": "ADA News",
            "url": "https://www.ada.org/en/publications/ada-news/rss-feed",
            "enabled": True
        },
        {
            "name": "PubMed - Digital Dentistry",
            "url": "https://pubmed.ncbi.nlm.nih.gov/?term=digital+dentistry&sort=date&format=rss",
            "enabled": True
        }
    ]
}

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 创建默认配置文件
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        print(f"已创建默认配置文件: {CONFIG_FILE}")
        print("请编辑配置文件，填入你的 Telegram Bot Token 和 Chat ID")
        return DEFAULT_CONFIG

def load_last_check():
    """加载上次检查时间"""
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_last_check(last_check):
    """保存上次检查时间"""
    with open(LAST_CHECK_FILE, 'w', encoding='utf-8') as f:
        json.dump(last_check, f, indent=2)

def fetch_rss_feed(url):
    """获取 RSS feed"""
    try:
        feed = feedparser.parse(url)
        return feed
    except Exception as e:
        print(f"获取 RSS 失败 ({url}): {e}")
        return None

def contains_keywords(text, keywords):
    """检查文本是否包含关键词"""
    if not text:
        return False
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False

def send_telegram_message(bot_token, chat_id, message):
    """发送 Telegram 消息"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"发送 Telegram 消息失败: {e}")
        return False

def check_rss_sources(config, last_check):
    """检查所有 RSS 源"""
    new_articles = []
    current_time = datetime.now()
    
    for source in config['rss_sources']:
        if not source.get('enabled', True):
            continue
            
        source_name = source['name']
        source_url = source['url']
        
        print(f"检查 {source_name}...")
        
        # 获取上次检查时间
        last_check_time = last_check.get(source_name, "1970-01-01T00:00:00")
        last_check_dt = datetime.fromisoformat(last_check_time.replace('Z', '+00:00'))
        
        # 获取 RSS feed
        feed = fetch_rss_feed(source_url)
        if not feed or not feed.entries:
            print(f"  跳过 {source_name} (无数据)")
            continue
        
        # 检查新文章
        source_new_articles = []
        for entry in feed.entries:
            # 获取文章发布时间
            published = getattr(entry, 'published', getattr(entry, 'updated', ''))
            if not published:
                continue
                
            try:
                # 尝试解析不同格式的时间
                pub_dt = None
                for date_format in ['%Y-%m-%dT%H:%M:%SZ', '%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%d %H:%M:%S']:
                    try:
                        pub_dt = datetime.strptime(published, date_format)
                        break
                    except ValueError:
                        continue
                        
                if not pub_dt:
                    pub_dt = datetime.now()  # 如果无法解析，当作最新
                    
            except Exception:
                pub_dt = datetime.now()
            
            # 检查是否是新文章
            if pub_dt > last_check_dt:
                # 检查是否包含关键词
                title = getattr(entry, 'title', '')
                summary = getattr(entry, 'summary', '')
                content = getattr(entry, 'content', [{}])[0].get('value', '') if entry.get('content') else ''
                
                full_text = f"{title} {summary} {content}"
                if contains_keywords(full_text, config['keywords']):
                    article = {
                        'source': source_name,
                        'title': title,
                        'link': entry.link,
                        'published': published,
                        'summary': summary[:200] + "..." if len(summary) > 200 else summary
                    }
                    source_new_articles.append(article)
        
        if source_new_articles:
            print(f"  发现 {len(source_new_articles)} 篇新文章")
            new_articles.extend(source_new_articles)
        else:
            print(f"  无新文章")
    
    # 更新最后检查时间
    last_check[source_name] = current_time.isoformat()
    
    return new_articles, last_check

def format_telegram_message(articles):
    """格式化 Telegram 消息"""
    if not articles:
        return None
        
    message = "🦷 <b>齿科数字化资讯更新</b>\n\n"
    
    for article in articles[:10]:  # 最多显示10篇文章
        message += f"📰 <b>{article['source']}</b>\n"
        message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
        if article['summary']:
            message += f"📝 {article['summary']}\n"
        message += f"⏰ {article['published']}\n\n"
    
    if len(articles) > 10:
        message += f"... 还有 {len(articles) - 10} 篇文章\n"
    
    return message

def main():
    """主函数"""
    print("🦷 齿科数字化 RSS 监控启动...")
    
    # 加载配置
    config = load_config()
    
    # 检查必要配置
    if config['telegram_bot_token'] == "YOUR_TELEGRAM_BOT_TOKEN":
        print("❌ 请先配置 Telegram Bot Token 和 Chat ID")
        return
    
    # 加载上次检查时间
    last_check = load_last_check()
    
    # 检查 RSS 源
    new_articles, updated_last_check = check_rss_sources(config, last_check)
    
    if new_articles:
        print(f"发现 {len(new_articles)} 篇相关文章")
        
        # 格式化消息
        message = format_telegram_message(new_articles)
        if message:
            # 发送 Telegram 消息
            success = send_telegram_message(
                config['telegram_bot_token'],
                config['telegram_chat_id'],
                message
            )
            if success:
                print("✅ Telegram 消息发送成功")
            else:
                print("❌ Telegram 消息发送失败")
    else:
        print("📭 无新文章")
    
    # 保存最后检查时间
    save_last_check(updated_last_check)
    print("💾 已保存检查状态")

if __name__ == "__main__":
    main()