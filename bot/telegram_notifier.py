from telegram import Bot
from shared.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)