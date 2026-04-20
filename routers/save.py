from fastapi import APIRouter, HTTPException
from services.youtube import get_video_data, extract_video_id
from services.transcript import get_transcript
from services.claude import classify_video

router = APIRouter()

@router.post("/save")
async def save_video(data: dict):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Get real video data
    video = get_video_data(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Get real transcript
    transcript = get_transcript(video_id)
    if not transcript:
        transcript = video.get("description", "No transcript available")
    
    # Real AI classification
    mode = classify_video(transcript, video["title"])
    
    return {
        "video_id": video_id,
        "title": video["title"],
        "thumbnail": video["thumbnail"],
        "channel": video["channel"],
        "mode": mode,
        "transcript": transcript,
        "url": url
    }