import os
import time
from utils.logger import setup_logger
from uploader.sheets_logger import setup_sheets
from worker.scheduler import start_scheduler

logger = setup_logger()

if __name__ == '__main__':
    logger.info("Initializing Sheets and Scheduler...")
    setup_sheets()
    start_scheduler()

    # Process 유지
    while True:
        time.sleep(60)