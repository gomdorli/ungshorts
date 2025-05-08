import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # 봇 토큰
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")    # 알림 받을 채팅 ID

# YouTube
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SHEETS_ID = os.getenv("SHEETS_ID")

# 경로 설정
AUDIO_OUTPUT_PATH = os.getenv("AUDIO_OUTPUT_PATH", "output/audio/")
THUMBNAIL_OUTPUT_PATH = os.getenv("THUMBNAIL_OUTPUT_PATH", "output/thumbnails/")
VIDEO_OUTPUT_PATH = os.getenv("VIDEO_OUTPUT_PATH", "output/videos/")

# 스케줄 타임존
TIMEZONE = os.getenv("TIMEZONE", "Asia/Seoul")

# 서비스의 공개 도메인(URL)
# 예: https://your-app-name.onrender.com
DOMAIN = os.getenv("DOMAIN", "https://ungshorts-8m6e.onrender.com")

REDIS_URL         = os.getenv("REDIS_URL", "redis://localhost:6379/0")