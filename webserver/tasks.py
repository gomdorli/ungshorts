# tasks.py

import os
from redis import Redis
from rq import Queue
from shared.config import REDIS_URL, TELEGRAM_BOT_TOKEN
from content.content_scraper        import scrape_content_for_keywords
from content.tts_generator          import generate_tts_audio
from video.thumbnail_generator      import create_thumbnail
from video.video_editor             import create_video_from_content
from uploader.youtube_uploader      import upload_video_to_youtube
from uploader.sheets_logger         import log_to_sheets
from bot.telegram_notifier          import send_message

# Redis 큐 설정
redis_conn = Redis.from_url(REDIS_URL)
video_queue = Queue("video", connection=redis_conn)

def enqueue_video_job(topic: str, chat_id: str):
    """웹훅에서 호출: 작업 큐에 등록만 함."""
    # 작업을 enqueue 합니다.
    video_queue.enqueue(process_video_job, topic, chat_id)

def process_video_job(topic: str, chat_id: str):
    """워커가 꺼내 처리할 비디오 생성 & 업로드 작업."""
    try:
        send_message(chat_id, f"🎬 ‘{topic}’ 쇼츠 영상 생성 시작…")
        
        # 1) 콘텐츠 스크랩 & 요약
        content = scrape_content_for_keywords(topic)
        images  = content["images"]
        summary = content["summary"]
        
        # 2) TTS
        audio_path = generate_tts_audio(summary, topic)
        # 3) 썸네일
        thumbnail = create_thumbnail(topic)
        # 4) 비디오
        video_path = create_video_from_content(images, audio_path, thumbnail, topic)
        # 5) 업로드
        video_id   = upload_video_to_youtube(video_path, f"{topic} - Shorts", summary, thumbnail)
        video_url  = f"https://youtu.be/{video_id}"
        # 6) 시트 기록
        log_to_sheets(topic, summary, video_url)
        # 7) 완료 알림
        send_message(chat_id, f"✅ 완료! 영상 링크: {video_url}")
    except Exception as e:
        # 1회 실패로만 처리하고, 재시도하지 않도록 raise 제거
        send_message(chat_id, f"❌ 쇼츠 생성 실패: {e}")