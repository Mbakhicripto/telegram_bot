import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# گرفتن توکن از محیط (Render Env Vars)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تابع /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات با موفقیت روی Render اجرا شد 😎")

# اجرای وب‌سرور ساده برای Render (فقط برای اینکه پورت باز باشه)
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست! ✅"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# اجرای ربات تلگرام
async def main():
    # راه‌اندازی ربات
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # اجرا در حالت polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

    await application.stop()
    await application.shutdown()

if __name__ == '__main__':
    # اجرای وب‌سرور در نخ جدا برای Render
    threading.Thread(target=run_web).start()

    # اجرای async main
    asyncio.run(main())
