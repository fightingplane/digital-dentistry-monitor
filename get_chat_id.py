#!/usr/bin/env python3
"""
Get Telegram Chat ID by listening for messages to your bot
"""
import os
import json
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Load config
config_path = "rss_config.json"
with open(config_path, 'r') as f:
    config = json.load(f)

BOT_TOKEN = config['telegram']['bot_token']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name if update.effective_user else "Unknown"
    
    message = f"✅ Chat ID 获取成功!\n\n"
    message += f"**Chat ID**: `{chat_id}`\n"
    message += f"**User**: {user_name}\n\n"
    message += f"请将这个 Chat ID 复制到你的 `rss_config.json` 文件中。"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def echo_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo back the chat ID for any message."""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")

def main():
    """Start the bot."""
    print("🤖 启动 Telegram Bot 来获取 Chat ID...")
    print("请在 Telegram 中向你的 bot 发送任意消息或 /start 命令")
    print("Bot 会回复你的 Chat ID\n")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_chat_id))
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()