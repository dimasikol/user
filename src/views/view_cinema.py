from fastapi import APIRouter

router = APIRouter()


@router.get('/cinema', tags=['cinema'])
async def cinema_page():

    return {"cinema": 'pass'}