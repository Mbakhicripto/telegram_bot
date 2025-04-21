import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # یا مستقیماً: "8084:..."

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://your-railway-subdomain.up.railway.app{WEBHOOK_PATH}"  # آدرس Railway

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات تلگرام روی Railway اجرا می‌شود ✅"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات روی Railway فعاله ✅")

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

async def run_bot():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.start()

import threading, asyncio
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
asyncio.run(run_bot())
