import os
import time
from scheduler import start_scheduler
from bot.telegram_bot import start_telegram_bot
from utils.logger import setup_logger
from uploader.sheets_logger import setup_sheets
from stats.stats_manager import monitor_video_stats, send_weekly_report

def main():
    logger = setup_logger()
    logger.info("Starting YouTube Shorts Bot...")
    
    setup_sheets()
    start_scheduler()

    logger.info("Telegram bot is starting...")
    start_telegram_bot()
    
    logger.info("Keeping process alive to avoid restart.")
    
    # Render가 프로세스를 종료하지 않도록 대기 루프 유지
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
