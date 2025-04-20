import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "tele1388_bot"
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = f"https://your-render-service.onrender.com{WEBHOOK_PATH}"  # اینو با آدرس رندر خودت جایگزین کن

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

@app.route("/")
def home():
    return "ربات آماده است ✅"

@app.post(WEBHOOK_PATH)
async def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات با موفقیت از طریق Webhook راه‌اندازی شد ✅")

# ثبت دستور
application.add_handler(CommandHandler("start", start))

# راه‌اندازی Webhook
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import threading
    import asyncio

    # اجرای Flask
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()

    # ثبت وب‌هوک و اجرای ربات
    asyncio.run(set_webhook())
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "tele1388_bot"
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = f"https://your-render-service.onrender.com{WEBHOOK_PATH}"  # اینو با آدرس رندر خودت جایگزین کن

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

@app.route("/")
def home():
    return "ربات آماده است ✅"

@app.post(WEBHOOK_PATH)
async def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات با موفقیت از طریق Webhook راه‌اندازی شد ✅")

# ثبت دستور
application.add_handler(CommandHandler("start", start))

# راه‌اندازی Webhook
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import threading
    import asyncio

    # اجرای Flask
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()

    # ثبت وب‌هوک و اجرای ربات
    asyncio.run(set_webhook())
