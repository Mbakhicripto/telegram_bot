import os
import datetime
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# ====== تنظیمات اولیه ======
TOKEN = os.environ.get("BOT_TOKEN")  # در Render این مقدار ست می‌شود
bot = Bot(token=TOKEN)

app = Flask(__name__)

# ====== ذخیره تصاویر ======
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# ====== هندلرهای اصلی ======
def start(update, context):
    update.message.reply_text("سلام! عکس تحلیلی نمادها را با کپشن نماد بفرست، یا بنویس: /get SYMBOL")

def save_photo(update, context):
    caption = update.message.caption
    if not caption:
        update.message.reply_text("لطفاً در کپشن نام نماد را وارد کنید.")
        return

    symbol = caption.strip().upper()
    photo = update.message.photo[-1].get_file()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{symbol}_{timestamp}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)
    photo.download(custom_path=filepath)
    update.message.reply_text(f"عکس ذخیره شد: {filename}")

def get_photos(update, context):
    if len(context.args) != 1:
        update.message.reply_text("استفاده صحیح: /get SYMBOL")
        return

    symbol = context.args[0].strip().upper()
    matched_files = [
        fname for fname in os.listdir(IMAGE_DIR)
        if fname.upper().startswith(symbol + "_")
    ]

    if not matched_files:
        update.message.reply_text(f"عکسی با نماد {symbol} پیدا نشد.")
        return

    for fname in matched_files:
        with open(os.path.join(IMAGE_DIR, fname), "rb") as f:
            update.message.reply_photo(photo=f, caption=fname)

# ====== تنظیم Dispatcher ======
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("get", get_photos))
dispatcher.add_handler(MessageHandler(Filters.photo, save_photo))

# ====== Webhook endpoint ======
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# ====== صفحه تست ساده ======
@app.route("/", methods=["GET"])
def index():
    return "ربات در حال اجراست."

