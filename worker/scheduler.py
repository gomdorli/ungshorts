# scheduler.py

import os
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING
from apscheduler.triggers.cron import CronTrigger
from keywords.keyword_fetcher import fetch_trending_keywords_from_zum
from content.content_scraper import scrape_content_for_keywords
from content.tts_generator import generate_tts_audio
from video.thumbnail_generator import create_thumbnail
from video.video_editor import create_video_from_content
from uploader.youtube_uploader import upload_video_to_youtube
from uploader.sheets_logger import log_to_sheets
from stats.stats_manager import monitor_video_stats, send_weekly_report
from utils.logger import setup_logger
from shared.config import TIMEZONE

logger = setup_logger()

# —————————— 전역 스케줄러 선언 ——————————
tz = pytz.timezone("Asia/Seoul")
scheduler = BackgroundScheduler(timezone=tz)
# ———————————————————————————————

def automated_workflow():
    keywords = fetch_trending_keywords_from_zum()
    for kw in keywords:
        logger.info(f"Scheduled job: processing '{kw}'...")
        summary = scrape_content_for_keywords(kw)
        audio = generate_tts_audio(summary, kw)
        thumb = create_thumbnail(kw)
        video = create_video_from_content(summary, audio, thumb, kw)
        vid = upload_video_to_youtube(video, f"{kw} - Shorts", summary, thumb)
        url = f"https://youtu.be/{vid}"
        log_to_sheets(kw, summary, url)
        logger.info(f"Uploaded {url}")

def start_scheduler():
    global scheduler

    # 이미 실행 중인지 확인
    if scheduler.state == STATE_RUNNING:
        print("[scheduler] already running, skipping start", flush=True)
        return

    # job id 로 중복 등록 방지
    if not scheduler.get_job("automated_workflow"):
        scheduler.add_job(
            automated_workflow,
            CronTrigger(hour=8, timezone=tz),
            id="automated_workflow"
        )
    # 매일 오후 3시 조회수 모니터링
    if not scheduler.get_job("monitor_video_stats"):
        scheduler.add_job(
            monitor_video_stats,
            CronTrigger(hour=15, timezone=tz),
            id="monitor_video_stats"
        )
        
    # 매주 월요일 오전 10시 주간 보고
    if not scheduler.get_job("send_weekly_report"):
        scheduler.add_job(
            send_weekly_report,
            CronTrigger(day_of_week="mon", hour=10, timezone=tz),
            id="send_weekly_report"
        )

    scheduler.start()
    logger.info(f"Scheduler started with jobs: {[j.id for j in scheduler.get_jobs()]}")
