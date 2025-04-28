# stats/stats_manager.py

import os
import json
import datetime
import requests
from telegram import Bot
from googleapiclient.discovery import build

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # 따로 봇에 /start 해서 얻어야 함
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
STATS_FILE = "video_stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def monitor_video_stats():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    stats = load_stats()

    for video_id, info in stats.items():
        request = youtube.videos().list(part="statistics", id=video_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            view_count = int(response['items'][0]['statistics']['viewCount'])
            if view_count >= 100 and not info.get('notified'):
                send_telegram_message(f"🔥 [조회수 100+] 영상 알림: https://youtube.com/shorts/{video_id} ({view_count} views)")
                stats[video_id]['notified'] = True

    save_stats(stats)

def send_weekly_report():
    stats = load_stats()
    weekly_views = []

    for video_id, info in stats.items():
        created_at = datetime.datetime.strptime(info['created_at'], "%Y-%m-%d")
        if (datetime.datetime.now() - created_at).days <= 7:
            weekly_views.append((video_id, info.get('views', 0)))

    if weekly_views:
        sorted_views = sorted(weekly_views, key=lambda x: x[1], reverse=True)
        report = "📊 [YouTube Shorts 주간 통계]\n\n"
        for vid, views in sorted_views[:5]:
            report += f"- https://youtube.com/shorts/{vid} : {views} views\n"
    else:
        report = "📊 이번 주에는 새로운 영상 활동이 없습니다."

    send_telegram_message(report)

def send_telegram_message(text):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text)
