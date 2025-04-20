import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن از محیط
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"🎯 توکن: {BOT_TOKEN[:10]}...")

# ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ دریافت شد: /start")
    await update.message.reply_text("سلام! ربات فعاله :)")

# وب سرور
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست ✅"

async def main():
    app_tg = Application.builder().token(BOT_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))

    await app_tg.initialize()
    await app_tg.start()
    await app_tg.updater.start_polling()
    await app_tg.updater.idle()

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    asyncio.run(main())
