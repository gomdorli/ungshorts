import os
import threading
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
from webserver.tasks import process_video_job

# 로거
logger = setup_logger()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start 핸들러
def start(update: Update, context: CallbackContext):
    update.message.reply_text("안녕하세요! 주제를 보내주시면 유튜브 쇼츠를 생성합니다.")

# /generate <주제> 핸들러
def generate(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic = ' '.join(context.args)
    if not topic:
        return update.message.reply_text("사용법: /generate <주제>")

    update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
    threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()

# /trending 핸들러: 상위 키워드 가져와 영상 자동 생성
def trending(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.reply_text("🔍 상위 트렌딩 키워드를 가져오는 중입니다...")
    keywords = fetch_trending_keywords()
    if not keywords:
        return update.message.reply_text("❌ 트렌딩 키워드를 가져오지 못했습니다.")

    # 예시: 상위 5개 키워드
    top_n = 5
    selected = keywords[:top_n]
    update.message.reply_text(f"📈 상위 {top_n}개 키워드: {', '.join(selected)}")

    for topic in selected:
        update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
        threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()
        
# 텍스트 메시지 핸들러
def handle_topic(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic = update.message.text
    send_message(f"'{topic}' 주제로 쇼츠 영상을 생성합니다...")

    try:
        # 1) 콘텐츠 요약
        content = scrape_content_for_keywords(topic)
        images = content["images"]
        if not images:
            raise Exception("No images found for keyword")
            
        summary = content["summary"]
        print(f"[handle_topic] Using summary: {summary}", flush=True)  # 디버깅 로그
        
        # 2) TTS 오디오 생성    
        audio_path = generate_tts_audio(summary, topic)
        
        # 3) 썸네일 생성
        thumbnail_path = create_thumbnail(topic)
        
        # 4) 영상 생성
        video_path = create_video_from_content(images, audio_path, thumbnail_path, topic)
        
        # 5) 유튜브 업로드
        video_id = upload_video_to_youtube(video_path, f"{topic} - Shorts", summary, thumbnail_path)
        video_url = f"https://youtu.be/{video_id}"
        
        # 6) Google Sheets에 기록
        log_to_sheets(topic, summary, video_url)
        
        # 7) 완료 메시지
        send_message(f"완료! 영상 링크: {video_url}")
        logger.info(f"Uploaded video {video_url} for topic '{topic}'")
    except Exception as e:
        update.message.reply_text("❌ Failed to create video.")
        send_message(f"❌ Error creating video for {topic}: {e}")
        print(f"[handle_topic] Error: {e}", flush=True)

# 핸들러 등록 함수
def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("generate", generate))
    dispatcher.add_handler(CommandHandler("trending", trending))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_topic))

# 봇 시작 함수
def start_telegram_bot():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    register_handlers(dp)
    updater.start_polling()
    updater.idle()