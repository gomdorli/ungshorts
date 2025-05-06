import os
from telegram import Bot
from shared.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

def send_message(arg1, arg2=None):
    # arg2가 None이면 send_message(text) 형태
    # arg2가 있으면 send_message(chat_id, text) 형태
    if arg2 is None:
        chat_id = CHAT_ID
        text    = arg1
    else:
        chat_id = arg1
        text    = arg2

    if not BOT_TOKEN or not chat_id:
        print("Telegram bot token or chat ID is not set.", flush=True)
        return

    try:
        bot.send_message(chat_id=chat_id, text=text)
        print(f"Sent message to Telegram [{chat_id}]: {text}", flush=True)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}", flush=True)