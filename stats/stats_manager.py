import os
import json
import datetime
from googleapiclient.discovery import build
from bot.telegram_notifier import send_message
from shared.config import YOUTUBE_API_KEY, TELEGRAM_CHAT_ID

STATS_FILE = 'video_stats.json'

# JSON 로드

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

# JSON 저장
def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

# 영상별 조회수 모니터링

def monitor_video_stats():
    stats = load_stats()
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    for vid, data in stats.items():
        req = youtube.videos().list(part='statistics', id=vid)
        res = req.execute()
        views = int(res['items'][0]['statistics'].get('viewCount', 0))
        if views >= 100 and data.get('last_views', 0) < 100:
            send_message(TELEGRAM_CHAT_ID, f"🎉 https://youtu.be/{vid} 가 100뷰를 넘었습니다! 현재 조회수: {views}")
        stats[vid]['last_views'] = views
    save_stats(stats)

# 주간 보고서 발송

def send_weekly_report():
    stats = load_stats()
    week_ago = datetime.datetime.datetime.now() - datetime.timedelta(days=7)
    weekly = []
    for vid, data in stats.items():
        upload_time = datetime.datetime.datetime.fromisoformat(data['upload_time'])
        if upload_time >= week_ago:
            weekly.append((vid, data.get('last_views', 0)))
    if weekly:
        weekly.sort(key=lambda x: x[1], reverse=True)
        msg = "📊 [주간 통계]\n"
        for vid, views in weekly[:5]:
            msg += f"- https://youtu.be/{vid} : {views} views\n"
    else:
        msg = "📊 이번 주에 새로 업로드된 영상이 없습니다."
    send_message(TELEGRAM_CHAT_ID, msg)