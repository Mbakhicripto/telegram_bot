import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# توکن ربات
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ساخت اپ Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست ✅"

# مسیر دریافت آپدیت‌های تلگرام
@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return 'ok'

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات با موفقیت راه‌اندازی شد ✅")

# راه‌اندازی بات
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# راه‌اندازی webhook
async def set_webhook():
    webhook_url = f"https://tele1388-bot.onrender.com/webhook/{BOT_TOKEN}"
    await application.bot.set_webhook(webhook_url)

if __name__ == '__main__':
    # ست کردن وبهوک
    asyncio.run(set_webhook())
    # اجرای سرور
    app.run(host="0.0.0.0", port=10000)
