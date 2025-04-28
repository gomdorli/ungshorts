from scheduler import start_scheduler
from telegram.telegram_bot import start_telegram_bot
from utils.logger import setup_logger
from uploader.sheets_logger import setup_sheets
from stats.stats_manager import monitor_video_stats, send_weekly_report

def main():
    logger = setup_logger()
    logger.info("Starting YouTube Shorts Bot...")
    
    setup_sheets()
    start_scheduler()
    start_telegram_bot()

if __name__ == "__main__":
    main()
