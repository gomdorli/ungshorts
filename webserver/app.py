import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater
from bot.telegram_bot import register_handlers
from shared.config import TELEGRAM_BOT_TOKEN, TIMEZONE, DOMAIN

app = Flask(__name__)
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dp = updater.dispatcher
register_handlers(dp)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, updater.bot)
    updater.bot.process_update(update)
    return "OK"

if __name__ == '__main__':
    # 외부에 공개하는 URL은 443 포트를 쓰도록(포트 표기는 하지 않음)
    port = int(os.environ.get('PORT', 10000))
    updater.start_webhook(
        listen='0.0.0.0',
        port=port,
        url_path=TELEGRAM_BOT_TOKEN
    )
    updater.bot.setWebhook(f"https://{os.getenv('DOMAIN')}/{TELEGRAM_BOT_TOKEN}")
    app.run(host='0.0.0.0', port=port)