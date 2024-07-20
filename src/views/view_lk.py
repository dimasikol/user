from fastapi import APIRouter
router = APIRouter()


@router.get('/', tags=['home'])
async def home_page():
    return {"data": "Hello World!"}


