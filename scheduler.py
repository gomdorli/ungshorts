from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from keywords.keyword_fetcher import fetch_trending_keywords
from content.content_scraper import scrape_content_for_keywords
from content.tts_generator import generate_tts_audio
from video.video_editor import create_video_from_content
from video.thumbnail_generator import create_thumbnail
from uploader.youtube_uploader import upload_video_to_youtube
from stats.stats_manager     import monitor_video_stats, send_weekly_report
import pytz

# 타임존 설정 (Asia/Seoul)
tz = pytz.timezone("Asia/Seoul")

def automated_workflow():
    keywords = fetch_trending_keywords()
    for keyword in keywords:
        content = scrape_content_for_keywords(keyword)
        audio_path = generate_tts_audio(content['summary'], keyword)
        video_path = create_video_from_content(content['images'], audio_path, keyword)
        thumbnail_path = create_thumbnail(keyword)
        upload_video_to_youtube(video_path, thumbnail_path, keyword, content['summary'])

def start_scheduler():
    # BackgroundScheduler에 서울 타임존 적용
    scheduler = BackgroundScheduler(timezone=tz)
    
    scheduler.add_job(automated_workflow, CronTrigger(hour=8, timezone=tz))
    scheduler.add_job(monitor_video_stats, CronTrigger(hour=9, timezone=tz))
    scheduler.add_job(send_weekly_report, CronTrigger(day_of_week='mon', hour=10, timezone=tz))
    scheduler.start()
