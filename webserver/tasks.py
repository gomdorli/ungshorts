# tasks.py

from content.content_scraper        import scrape_content_for_keywords
from content.tts_generator          import generate_tts_audio
from video.thumbnail_generator      import create_thumbnail
from video.video_editor             import create_video_from_content
from uploader.youtube_uploader      import upload_video_to_youtube
from uploader.sheets_logger         import log_to_sheets
from bot.telegram_notifier          import send_message

def process_video_job(topic: str, chat_id: str):
    try:
        send_message(chat_id, f"🎬 ‘{topic}’ 쇼츠 생성 시작…")
        content   = scrape_content_for_keywords(topic)
        images    = content["images"]
        summary   = content["summary"]
        audio     = generate_tts_audio(summary, topic)
        thumbnail = create_thumbnail(topic)
        video     = create_video_from_content(images, audio, thumbnail, topic)
        vid_id    = upload_video_to_youtube(video, f"{topic} - Shorts", summary, thumbnail)
        url       = f"https://youtu.be/{vid_id}"
        log_to_sheets(topic, summary, url)
        send_message(chat_id, f"✅ 완료! 영상 링크: {url}")
    except Exception as e:
        send_message(chat_id, f"❌ 쇼츠 생성 실패: {e}")
