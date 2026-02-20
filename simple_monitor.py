#!/usr/bin/env python3
"""
简化版齿科数字化 RSS 监控
"""

import requests
import json
from datetime import datetime

# 你的配置
BOT_TOKEN = "8587699905:AAFPoaZhtvt9PfVZ3M2FygoXmp5z9j4mmNA"
CHAT_ID = "7896544619"

def send_test_message():
    """发送测试消息"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = "🦷 齿科数字化 RSS 监控系统已启动！\n\n我将定期检查以下资讯源：\n• Dental Economics\n• Dentistry Today\n• 3Shape Blog\n• PubMed 学术研究\n\n当发现相关更新时，我会立即通知你！"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram 测试消息发送成功")
            return True
        else:
            print(f"❌ 发送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False

if __name__ == "__main__":
    print("🚀 启动简化版 RSS 监控...")
    send_test_message()