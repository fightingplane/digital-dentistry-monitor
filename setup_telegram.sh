#!/bin/bash

echo "🦷 齿科数字化 RSS 监控 - Telegram 配置"
echo "========================================"

# 检查是否已有配置
if [ -f ".env" ]; then
    echo "✅ 已检测到现有配置文件"
    read -p "是否要更新配置? (y/N): " update
    if [[ ! $update =~ ^[Yy]$ ]]; then
        echo "📋 使用现有配置"
        exit 0
    fi
fi

echo ""
echo "请提供以下信息："
echo "1. Telegram Bot Token (从 @BotFather 获取)"
echo "2. Telegram Chat ID (可以是群组ID、频道ID或个人聊天ID)"

# 输入 Bot Token
read -p "Telegram Bot Token: " bot_token

# 输入 Chat ID
read -p "Telegram Chat ID: " chat_id

# 创建 .env 文件
cat > .env << EOF
TELEGRAM_BOT_TOKEN=$bot_token
TELEGRAM_CHAT_ID=$chat_id
EOF

echo ""
echo "✅ 配置已保存到 .env 文件"
echo "🔒 请确保 .env 文件不要提交到 Git"

# 设置文件权限
chmod 600 .env

echo ""
echo "🚀 现在可以运行监控脚本了！"
echo "运行命令: python3 rss_monitor.py"