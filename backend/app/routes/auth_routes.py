from fastapi import APIRouter
from app.models.user_model import UserRegister, UserLogin
from app.controllers.auth_controller import register_user, login_user

router = APIRouter()

@router.post("/auth/register", tags=["Auth"])
async def register(user: UserRegister):
    return await register_user(user)

@router.post("/auth/login", tags=["Auth"])
async def login(user: UserLogin):
    return await login_user(user)
