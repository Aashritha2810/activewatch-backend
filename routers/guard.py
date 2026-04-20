from fastapi import APIRouter

router = APIRouter()

limits = {}

@router.post("/set-guard-limit")
async def set_limit(data: dict):
    user_id = data.get("user_id", "default")
    limit = data.get("limit_minutes", 30)
    limits[user_id] = limit
    return {"success": True, "limit_minutes": limit}

@router.get("/get-guard-limit/{user_id}")
async def get_limit(user_id: str):
    return {"limit_minutes": limits.get(user_id, 30)}