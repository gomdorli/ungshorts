import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from shared.config import YOUTUBE_CLIENT_SECRETS_FILE

# YouTube 업로드
def upload_video_to_youtube(video_path, title, description, thumbnail_path=None):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    import google_auth_oauthlib.flow
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        YOUTUBE_CLIENT_SECRETS_FILE, scopes)
    credentials = flow.run_console()
    youtube = build("youtube", "v3", credentials=credentials)

    body = {
        'snippet': {'title': title, 'description': description, 'categoryId': '22'},
        'status': {'privacyStatus': 'public'}
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    req = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    res = req.execute()
    video_id = res['id']
    if thumbnail_path:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
    else:
        print(f"[WARN] thumbnail_path is None, skipping thumbnail upload", flush=True)
    return video_id