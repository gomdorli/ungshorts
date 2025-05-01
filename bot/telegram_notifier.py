
import os
import telegram

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

def send_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram bot token or chat ID is not set.", flush=True)
        return
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        print(f"Sent message to Telegram: {text}", flush=True)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}", flush=True)
