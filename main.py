import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# توکن از محیط
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET_PATH = BOT_TOKEN  # برای امنیت بیشتر می‌تونی چیز دیگه‌ای بزاری
WEBHOOK_URL = f"https://YOUR_RENDER_DOMAIN.onrender.com/{WEBHOOK_SECRET_PATH}"

# ---- Flask برای سلامت ----
app = Flask(__name__)

@app.route('/')
def home():
    return 'ربات در حال اجراست ✅'

@app.route(f'/{WEBHOOK_SECRET_PATH}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return 'ok'

# ---- ربات ----
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات شما با موفقیت روی Render راه‌اندازی شد.")

application.add_handler(CommandHandler("start", start))

async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

# ---- اجرای همه چیز ----
if __name__ == '__main__':
    import asyncio
    import threading

    # اجرای Flask در یک Thread
    def run_flask():
        app.run(host='0.0.0.0', port=10000)

    threading.Thread(target=run_flask).start()

    # اجرای Webhook
    asyncio.run(set_webhook())
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET_PATH,
    )
