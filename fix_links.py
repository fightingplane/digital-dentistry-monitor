#!/usr/bin/env python3
"""
修复 Telegram 消息中的链接格式
"""

import json

def fix_telegram_message_format():
    """修复消息格式，确保包含可点击链接"""
    
    # 测试消息格式
    test_articles = [
        {
            'source': 'Dental Economics',
            'title': 'A-dec and Dentsply Sirona Expand Partnership',
            'link': 'https://www.dentaleconomics.com/a-dec-and-dentsply-sirona-expand-partnership/',
            'published': '2026-02-20',
            'summary': '两家牙科设备巨头扩大合作，涉及数字化工作流程整合，将为诊所提供更完整的数字解决方案。',
            'priority_emoji': '🔴',
            'priority': 'high'
        },
        {
            'source': 'Dentistry Today',
            'title': 'Kuraray Launches CERABIEN MiLai Ceramic System',
            'link': 'https://www.dentistrytoday.com/kuraray-launches-cerabien-milai-ceramic-system/',
            'published': '2026-02-20',
            'summary': '新的陶瓷材料系统适用于CAD/CAM数字化制作，提供更好的美学效果和机械性能。',
            'priority_emoji': '🟡',
            'priority': 'medium'
        }
    ]
    
    # 正确的 Telegram HTML 格式
    message = "🦷 <b>齿科数字化资讯更新（修复链接版）</b>\n\n"
    
    for article in test_articles:
        message += f"{article['priority_emoji']} <b>{article['source']}</b>\n"
        message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
        if article['summary']:
            message += f"📝 {article['summary']}\n"
        message += f"⏰ {article['published']}\n\n"
    
    return message

if __name__ == "__main__":
    message = fix_telegram_message_format()
    print("修复后的消息格式:")
    print(message)
    
    # 保存到文件用于测试
    with open('fixed_message_test.txt', 'w', encoding='utf-8') as f:
        f.write(message)
    
    print("✅ 消息格式已保存到 fixed_message_test.txt")