import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot.telegram_bot import register_handlers
from shared.config import TELEGRAM_BOT_TOKEN, DOMAIN

# 환경 변수
TOKEN  = TELEGRAM_BOT_TOKEN
DOMAIN = DOMAIN  # DOMAIN에는 포트 없이 순수 도메인만

# Webhook URL 구성
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL  = f"https://{DOMAIN}{WEBHOOK_PATH}"

# Bot & Dispatcher 초기화
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)
register_handlers(dispatcher)

# Flask 앱 설정
app = Flask(__name__)

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# 앱 로드시 한 번만 Webhook 등록
# (Gunicorn이 import할 때 실행됩니다)
bot.set_webhook(WEBHOOK_URL)
print("Set webhook to", WEBHOOK_URL, flush=True)

# Gunicorn이 이 app 객체를 사용해 서비스합니다.
