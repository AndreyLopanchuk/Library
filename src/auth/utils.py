from fastapi import Response

from src.auth.schemas.token_schema import TokenSchema
from src.core.config import settings


def set_in_cookie(response: Response, token: str, max_age: int):
    response.set_cookie(key="refresh_token", value=token, httponly=True, samesite="strict", max_age=max_age)


def set_auth_tokens(response: Response, tokens: dict):
    set_in_cookie(
        token=tokens["refresh_token"], max_age=settings.auth_jwt.refresh_token_expire_seconds, response=response
    )

    return TokenSchema(access_token=tokens["access_token"], token_type="bearer")
