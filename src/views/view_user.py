from fastapi import APIRouter, Body, Request
from pydantic import BaseModel,EmailStr

router = APIRouter()

data = []
@router.get("/users")
async def get_users():
    return {"data": data}


@router.get("/users/{user_id}")
async def get_user(user_id):
    return {"data": data[user_id]}


@router.get("/register")
async def register(request: Request):
    query_param = request.query_params
    form_data = await request.form()
    return {"data": request.query_params}

