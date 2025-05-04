import time
from utils.logger import setup_logger
from uploader.sheets_logger import setup_sheets
from bot.telegram_bot import start_telegram_bot
from worker.scheduler import start_scheduler

logger = setup_logger()

if __name__ == '__main__':
    logger.info("Initializing Sheets and Scheduler...")
    setup_sheets()
    start_scheduler()
    
    # 텔레그램 봇은 RUN_TELEGRAM_BOT 환경 변수가 true일 때만 실행
    if os.getenv("RUN_TELEGRAM_BOT", "false").lower() == "true":
        from bot.telegram_bot import start_telegram_bot
        logger.info("Starting Telegram bot (polling)...")
        start_telegram_bot()
    else:
        logger.info("RUN_TELEGRAM_BOT is false — skipping polling bot.")
        
    # Process 유지
    while True:
        time.sleep(60)