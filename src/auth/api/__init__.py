from fastapi import APIRouter, Depends

from src.auth.api.auth_routes import router as auth_router, http_bearer
from src.auth.api.user_routes import router as user_router

security_router = APIRouter()

security_router.include_router(auth_router)
security_router.include_router(user_router)
