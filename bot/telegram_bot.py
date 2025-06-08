from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Dispatcher
from keywords.fetch_related_keywords import fetch_related_keywords
from keywords.keyword_fetcher import fetch_trending_keywords_from_zum
from webserver.tasks import process_video_job
import threading

def handle_generate(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic_input = ' '.join(context.args).strip()

    if topic_input:
        update.message.reply_text(f"🔍 ‘{topic_input}’ 기반 트렌드 키워드 수집 중...")
        keywords = fetch_related_keywords([topic_input])
        if not keywords:
            update.message.reply_text("⚠️ Google Trends 실패 → Naver 시도 중...")
            keywords = fetch_trending_keywords_from_zum()
        if not keywords:
            update.message.reply_text("❌ 키워드를 수집하지 못했습니다.")
            return
        selected = keywords[:3]
    else:
        update.message.reply_text("📈 트렌드 키워드 자동 수집 중...")
        keywords = fetch_related_keywords()
        if not keywords:
            update.message.reply_text("⚠️ Google Trends 실패 → Naver 시도 중...")
            keywords = fetch_trending_keywords_from_zum()
        if not keywords:
            update.message.reply_text("❌ 키워드를 수집하지 못했습니다.")
            return
        selected = keywords[:3]

    update.message.reply_text(f"📌 생성 키워드: {', '.join(selected)}")
    for topic in selected:
        update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
        threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()


def handle_topic(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    topic = update.message.text.strip()
    if topic.startswith("/"):
        return
    update.message.reply_text(f"🎬 ‘{topic}’ 영상 생성 시작...")
    threading.Thread(target=process_video_job, args=(topic, chat_id), daemon=True).start()


def register_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler("generate", handle_generate))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_topic))
