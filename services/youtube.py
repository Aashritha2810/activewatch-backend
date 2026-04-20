import requests
import os
from dotenv import load_dotenv
load_dotenv()

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def get_video_data(video_id):
    r = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "id": video_id,
            "key": os.getenv("YOUTUBE_API_KEY"),
            "part": "snippet"
        }
    )
    data = r.json()
    if not data.get("items"):
        return None
    snippet = data["items"][0]["snippet"]
    return {
        "title": snippet["title"],
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "channel": snippet["channelTitle"],
        "description": snippet.get("description", "")
    }