import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from keywords.keyword_fetcher import fetch_trending_keywords
from content.content_scraper import scrape_content_for_keywords
from content.tts_generator import generate_tts_audio
from video.thumbnail_generator import create_thumbnail
from video.video_editor import create_video_from_content
from uploader.youtube_uploader import upload_video_to_youtube
from uploader.sheets_logger import log_to_sheets
from bot.telegram_notifier import send_message
from utils.logger import setup_logger

# 로거
logger = setup_logger()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start 핸들러
def start(update: Update, context: CallbackContext):
    update.message.reply_text("안녕하세요! 주제를 보내주시면 유튜브 쇼츠를 생성합니다.")
    logger.info(f"New chat: {update.message.chat_id}")

# 텍스트 메시지 핸들러

def handle_topic(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic = update.message.text.strip()
    send_message(chat_id, f"'{topic}' 주제로 쇼츠 영상을 생성합니다...")

    # 1) 콘텐츠 요약
    summary = scrape_content_for_keywords(topic)
    # 2) TTS 오디오 생성
    audio_path = generate_tts_audio(summary, topic)
    # 3) 썸네일 생성
    thumbnail_path = create_thumbnail(topic)
    # 4) 영상 생성
    video_path = create_video_from_content(summary, audio_path, thumbnail_path, topic)
    # 5) 유튜브 업로드
    video_id = upload_video_to_youtube(video_path, f"{topic} - Shorts", summary, thumbnail_path)
    video_url = f"https://youtu.be/{video_id}"
    # 6) Google Sheets에 기록
    log_to_sheets(topic, summary, video_url)
    # 7) 완료 메시지
    send_message(chat_id, f"완료! 영상 링크: {video_url}")
    logger.info(f"Uploaded video {video_url} for topic '{topic}'")

# 핸들러 등록 함수
def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_topic))

# 봇 시작 함수
def start_telegram_bot():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    register_handlers(dp)
    updater.start_polling()
    updater.idle()