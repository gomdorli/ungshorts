import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater
from bot.telegram_bot import register_handlers
from shared.config import TELEGRAM_BOT_TOKEN, TIMEZONE, DOMAIN

app = Flask(__name__)
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
register_handlers(updater.dispatcher)

# 외부에 노출될 webhook 경로
WEBHOOK_PATH = f"/{TELEGRAM_BOT_TOKEN}"
# 텔레그램 서버에 등록할 URL (포트 없이!)
WEBHOOK_URL  = f"https://{DOMAIN}{WEBHOOK_PATH}"

# Render가 할당한 내부 포트 (예: 10000)
port = int(os.environ.get("PORT", 10000))

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, updater.bot)
    updater.bot.process_update(update)
    return "OK"

if __name__ == "__main__":
    # 1) 내부 포트(listen, port) 2) 외부 URL(webhook_url)
    updater.start_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=WEBHOOK_URL,
    )
    # Flask도 동일 포트로 실행
    app.run(host="0.0.0.0", port=port)
