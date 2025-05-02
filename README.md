# YouTube Shorts 자동 생성 프로젝트

## 환경 변수 설정
- TELEGRAM_BOT_TOKEN: Telegram Bot API 토큰
- TELEGRAM_CHAT_ID: 알림 수신용 채팅 ID
- YOUTUBE_CLIENT_SECRETS_FILE: OAuth 클라이언트 시크릿 JSON 경로
- YOUTUBE_API_KEY: YouTube Data API 키
- GOOGLE_SERVICE_ACCOUNT_JSON: Google Service Account JSON (base64 또는 raw)
- SHEETS_ID: Google Sheets 스프레드시트 ID
- DOMAIN: Webhook 도메인 예) example.onrender.com
- TIMEZONE: Asia/Seoul (기본)

## 배포
1. Web Service: `python webserver/app.py`
2. Worker: `python worker/main.py`
3. Render 환경: 무료 Web Service + Background Worker