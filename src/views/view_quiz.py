from fastapi import APIRouter

router = APIRouter()

@router.get("/quiz")
async def get_quiz():
    return {"message": "Quiz API"}