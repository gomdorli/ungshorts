# uploader/youtube_uploader.py

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_video_to_youtube(video_path, thumbnail_path, title, description):
    youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [title, "Shorts"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False
        }
    }

    media_file = MediaFileUpload(video_path, resumable=True, mimetype='video/*')
    upload_request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file)
    response = upload_request.execute()

    if thumbnail_path:
        youtube.thumbnails().set(videoId=response['id'], media_body=MediaFileUpload(thumbnail_path)).execute()

    return response['id']
