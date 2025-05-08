import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from bot.telegram_bot import register_handlers
from tasks import enqueue_video_job
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
    # 1) 메시지는 디스패처로 처리하되…
    dispatcher.process_update(update)
    # 2) 핸들러 내부에서 비디오 작업을 바로 만들지 않고, 큐에 등록
    #    (handle_topic 내부 말고, telegram_notifier로 chat_id까지 파싱해서)
    topic   = update.message.text
    chat_id = update.message.chat_id
    enqueue_video_job(topic, chat_id)
    return "OK"

# 앱 로드시 한 번만 Webhook 등록
# (Gunicorn이 import할 때 실행됩니다)
bot.set_webhook(WEBHOOK_URL)
print("Set webhook to", WEBHOOK_URL, flush=True)

# Gunicorn이 이 app 객체를 사용해 서비스합니다.
