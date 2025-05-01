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
from apscheduler.triggers.date import DateTrigger
import datetime

# —————————— 전역 스케줄러 선언 ——————————
tz = pytz.timezone("Asia/Seoul")
scheduler = BackgroundScheduler(timezone=tz)
# ———————————————————————————————

def automated_workflow():
    keywords = fetch_trending_keywords()
    for keyword in keywords:
        content = scrape_content_for_keywords(keyword)
        audio_path = generate_tts_audio(content['summary'], keyword)
        video_path = create_video_from_content(content['images'], audio_path, keyword)
        thumbnail_path = create_thumbnail(keyword)
        upload_video_to_youtube(video_path, thumbnail_path, keyword, content['summary'])

def start_scheduler():
    global scheduler
    
    # ② 이미 시작된 상태라면 아무것도 하지 않음
    if scheduler.state == scheduler.STATE_RUNNING:
        print("[scheduler] already running, skipping start", flush=True)
        return

    # ③ 잡을 add_job 할 때도 id를 붙여두면 중복 추가 방지
    if not scheduler.get_job("automated_workflow"):
        scheduler.add_job(automated_workflow,
                          CronTrigger(hour=8, timezone=tz),
                          id="automated_workflow")
    if not scheduler.get_job("monitor_video_stats"):
        scheduler.add_job(monitor_video_stats,
                          CronTrigger(hour=9, timezone=tz),
                          id="monitor_video_stats")
    if not scheduler.get_job("send_weekly_report"):
        scheduler.add_job(send_weekly_report,
                          CronTrigger(day_of_week="mon", hour=10, timezone=tz),
                          id="send_weekly_report")

    scheduler.start()
    print("[scheduler] started with jobs:", [j.id for j in scheduler.get_jobs()], flush=True)