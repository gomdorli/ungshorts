# telegram/telegram_bot.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from content.tts_generator import generate_tts_audio
from video.video_editor import create_video_from_content
from uploader.youtube_uploader import upload_video_to_youtube

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Send a topic and I will create a YouTube Shorts!')
    print(f"Your Chat ID is: {update.message.chat_id}", flush=True)

def handle_message(update: Update, context: CallbackContext):
    keyword = update.message.text
    audio_path = generate_tts_audio(f"A trending topic: {keyword}", keyword)
    video_path = create_video_from_content([], audio_path, keyword)
    video_id = upload_video_to_youtube(video_path, None, keyword, f"Shorts about {keyword}")
    update.message.reply_text(f"Shorts uploaded! https://youtube.com/shorts/{video_id}")

def start_telegram_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
