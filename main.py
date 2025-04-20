import os
import json
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# گرفتن توکن از محیط
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ساخت URL وب‌هوک
WEBHOOK_URL = f"https://tele1388_bot.onrender.com/{BOT_TOKEN}"

# Flask app برای پاسخ‌دهی به Webhook
app = Flask(__name__)

# متغیر سراسری برای application (داخل set_webhook مقدار می‌گیره)
application = None

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات با موفقیت روی Render اجرا شده است!")

# مسیری که Telegram برای Webhook به آن پیام می‌فرستد
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = Update.de_json(json.loads(json_data), application.bot)
    asyncio.create_task(application.process_update(update))
    return "OK"

# اجرای Flask در نخ جداگانه
def run_web():
    app.run(host="0.0.0.0", port=10000)

# راه‌اندازی ربات و ثبت Webhook
async def set_webhook():
    global application
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    # اجرای سرور Flask در نخ جدا
    threading.Thread(target=run_web).start()
    # راه‌اندازی Webhook و ربات
    asyncio.run(set_webhook())
