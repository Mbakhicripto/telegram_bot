import os
import json
import asyncio
import threading  # وارد کردن threading برای اجرای سرور وب در نخ جدا
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# گرفتن توکن از محیط (Render Env Vars)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تنظیم URL برای Webhook
WEBHOOK_URL = f"https://tele1388-bot.onrender.com/{BOT_TOKEN}"

# تابع /start
async def start(update: Update, context):
    await update.message.reply_text("سلام! ربات با موفقیت روی Render در حال اجراست.")

# ایجاد و تنظیم Flask برای Webhook
app = Flask(__name__)

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json.loads(json_str), application.bot)
    application.update_queue.put(update)
    return "OK", 200

def run_web():
    app.run(host='0.0.0.0', port=10000)

async def set_webhook():
    # راه‌اندازی ربات
    application = Application.builder().token(BOT_TOKEN).build()

    # تنظیم Webhook
    await application.bot.set_webhook(WEBHOOK_URL)

    # اضافه کردن handler برای دستور start
    application.add_handler(CommandHandler("start", start))

    # اجرای ربات
    await application.initialize()
    await application.start_polling()
    await application.idle()

    await application.stop()
    await application.shutdown()

if __name__ == '__main__':
    # اجرای وب‌سرور در نخ جدا برای Render
    threading.Thread(target=run_web).start()

    # تنظیم Webhook و شروع ربات
    asyncio.run(set_webhook())
