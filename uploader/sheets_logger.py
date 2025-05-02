import os
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials
from stats.stats_manager import save_stats

SHEETS_CLIENT = None
SHEETS_ID = None

# 초기화 함수

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

# 시트에 로그 및 stats 파일 업데이트
def log_to_sheets(topic, summary, video_url):
    sheet = SHEETS_CLIENT.open_by_key(SHEETS_ID).sheet1
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, topic, summary, video_url])

    # stats 파일 업데이트
    video_id = video_url.split('/')[-1]
    stats = {}
    if os.path.exists('video_stats.json'):
        with open('video_stats.json', 'r') as f:
            stats = json.load(f)
    stats[video_id] = {
        'upload_time': datetime.datetime.now().isoformat(),
        'last_views': 0
    }
    save_stats(stats)