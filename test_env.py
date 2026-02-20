#!/usr/bin/env python3
"""
测试环境变量配置
"""

import os

def test_environment_variables():
    """测试环境变量是否正确设置"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print("🔍 环境变量测试:")
    if bot_token:
        print(f"✅ TELEGRAM_BOT_TOKEN: {bot_token[:10]}...{bot_token[-5:]}")
    else:
        print("❌ TELEGRAM_BOT_TOKEN 未设置")
        
    if chat_id:
        print(f"✅ TELEGRAM_CHAT_ID: {chat_id}")
    else:
        print("❌ TELEGRAM_CHAT_ID 未设置")
    
    # 测试 Telegram 连接
    if bot_token and chat_id:
        try:
            import requests
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": "✅ 安全版本测试成功！环境变量配置正确。",
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram 连接测试成功")
                return True
            else:
                print(f"❌ Telegram 连接失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Telegram 连接异常: {e}")
            return False
    else:
        print("⚠️  跳过 Telegram 测试（缺少凭据）")
        return False

if __name__ == "__main__":
    test_environment_variables()