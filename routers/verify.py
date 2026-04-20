from fastapi import APIRouter, HTTPException
from services.claude import verify_answer

router = APIRouter()

@router.post("/verify-answer")
async def verify(data: dict):
    question = data.get("question")
    user_answer = data.get("user_answer")
    correct_answer = data.get("correct_answer")
    
    if not all([question, user_answer, correct_answer]):
        raise HTTPException(status_code=400, detail="question, user_answer, correct_answer required")
    
    result = verify_answer(question, user_answer, correct_answer)
    return result