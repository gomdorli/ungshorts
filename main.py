import os
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

    if os.getenv("RUN_TELEGRAM_BOT", "false").lower() == "true":
        logger.info("Telegram bot is starting...")
        start_telegram_bot()
    else:
        logger.info("Telegram bot is disabled.")

if __name__ == "__main__":
    main()
