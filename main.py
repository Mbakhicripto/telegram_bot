import os
import threading
import asyncio
import logging
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# لاگ‌گیری فعال
logging.basicConfig(level=logging.INFO)

# گرفتن توکن از محیط (Render Env Vars)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ توکن BOT_TOKEN تنظیم نشده!")

# تابع /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"📩 دریافت شد از {update.effective_user.username}: {update.message.text}")
    await update.message.reply_text("سلام! ربات با موفقیت روی Render اجرا شد ✅")

# اجرای وب‌سرور ساده برای Render (فقط برای اینکه پورت باز باشه)
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست! ✅"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# اجرای ربات تلگرام
async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    asyncio.run(main())
