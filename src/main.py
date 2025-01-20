from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse

from src.app.api import app_router
from src.auth.api import security_router
from src.auth.api.auth_routes import http_bearer  # , router as auth_router

from src.core.database.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
    yield
    await db.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)


main_app.include_router(router=app_router, dependencies=[Depends(http_bearer)])
main_app.include_router(router=security_router)
