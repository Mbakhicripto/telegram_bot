from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
import os
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من روی Render هستم :)")

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

    # وقتی کار تموم شد:
    await application.stop()
    await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
