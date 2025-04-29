# uploader/sheets_logger.py

import os
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials

SHEETS_CLIENT = None
SHEETS_ID = None

def setup_sheets():
    global SHEETS_CLIENT, SHEETS_ID
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    SHEETS_CLIENT = gspread.authorize(creds)
    SHEETS_ID = os.getenv("SHEETS_ID")

def log_to_sheets(topic, summary, video_url):
    sheet = SHEETS_CLIENT.open_by_key(SHEETS_ID).sheet1
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, topic, summary, video_url])
