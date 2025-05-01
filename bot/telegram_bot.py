
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from content.tts_generator import generate_tts_audio
from content.content_scraper import scrape_content_for_keywords
from video.video_editor import create_video_from_content
from uploader.youtube_uploader import upload_video_to_youtube
from bot.telegram_notifier import send_message

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Send a topic and I will create a YouTube Shorts!')
    print(f"Your Chat ID is: {update.message.chat_id}", flush=True)

def handle_message(update: Update, context: CallbackContext):
    print("[handle_message] Triggered", flush=True)
    keyword = update.message.text
    print(f"[handle_message] Received keyword: {keyword}", flush=True)
    try:
        send_message(f"🎬 Generating video for: {keyword}")
        
        content = scrape_content_for_keywords(keyword)
        images = content["images"]
        if not images:
            raise Exception("No images found for keyword")

        audio_path = generate_tts_audio(content["summary"], keyword)
        video_path = create_video_from_content(images, audio_path, keyword)
        video_id = upload_video_to_youtube(video_path, None, keyword, f"Shorts about {keyword}")
        msg = f"✅ Shorts uploaded!\nhttps://youtube.com/shorts/{video_id}"
        update.message.reply_text(msg)
        send_message(msg)
        print(f"[handle_message] Successfully uploaded video: {video_id}", flush=True)

    except Exception as e:
        update.message.reply_text("❌ Failed to create video.")
        send_message(f"❌ Error creating video for {keyword}: {e}")
        print(f"[handle_message] Error: {e}", flush=True)

_started = False

def start_telegram_bot():
    global _started
    if _started:
        print("[telegram_bot] already running, skip", flush=True)
        return

    _started = True
    updater = Updater(TOKEN, use_context=True)
    # … 핸들러 등록 …
    updater.start_polling()
    updater.idle()
