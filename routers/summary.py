from fastapi import APIRouter, HTTPException
from services.claude import generate_summary

router = APIRouter()

@router.post("/generate-summary")
async def summarize(data: dict):
    transcript = data.get("transcript")
    title = data.get("title")
    
    if not transcript:
        raise HTTPException(status_code=400, detail="transcript required")
    
    summary = generate_summary(transcript, title or "Unknown")
    return summary