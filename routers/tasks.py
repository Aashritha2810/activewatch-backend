from fastapi import APIRouter, HTTPException
from services.claude import generate_tasks

router = APIRouter()

@router.post("/generate-tasks")
async def create_tasks(data: dict):
    transcript = data.get("transcript")
    title = data.get("title")
    
    if not transcript or not title:
        raise HTTPException(status_code=400, detail="transcript and title required")
    
    tasks = generate_tasks(transcript, title)
    return tasks