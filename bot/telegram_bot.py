import os
import threading
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from fetch_related_keywords import fetch_related_keywords
from keywords.keyword_fetcher import fetch_trending_keywords_from_naver
from content.content_scraper import scrape_content_for_keywords
from content.tts_generator import generate_tts_audio
from video.thumbnail_generator import create_thumbnail
from video.video_editor import create_video_from_content
from uploader.youtube_uploader import upload_video_to_youtube
from uploader.sheets_logger import log_to_sheets
from bot.telegram_notifier import send_message
from utils.logger import setup_logger
from webserver.tasks import process_video_job

# 로거
logger = setup_logger()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start 핸들러
def start(update: Update, context: CallbackContext):
    update.message.reply_text("안녕하세요! 주제를 보내주시면 유튜브 쇼츠를 생성합니다.")

# /generate 핸들러
def generate(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic_input = ' '.join(context.args).strip()

    if topic_input:
        update.message.reply_text(f"🔍 ‘{topic_input}’ 기반 트렌드 키워드 수집 중...")
        keywords = fetch_related_keywords([topic_input])
        if not keywords:
            update.message.reply_text("⚠️ Google Trends 실패 → Naver 시도 중...")
            keywords = fetch_trending_keywords_from_naver()
        if not keywords:
            update.message.reply_text("❌ 키워드를 수집하지 못했습니다.")
            return

        selected = keywords[:3]
        update.message.reply_text(f"📌 ‘{topic_input}’ 관련 키워드: {', '.join(selected)}")
        for topic in selected:
            update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
            threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()
        return

    update.message.reply_text("📈 트렌드 키워드 자동 수집 중...")
    keywords = fetch_related_keywords()
    if not keywords:
        update.message.reply_text("⚠️ Google Trends 실패 → Naver 시도 중...")
        keywords = fetch_trending_keywords_from_naver()
    if not keywords:
        update.message.reply_text("❌ 키워드를 수집하지 못했습니다.")
        return

    selected = keywords[:3]
    update.message.reply_text(f"📌 자동 키워드: {', '.join(selected)}")
    for topic in selected:
        update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
        threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()

# 텍스트 메시지 핸들러
def handle_topic(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic = update.message.text.strip()
    if topic.startswith("/"):
        return
    update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
    threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_topic))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
