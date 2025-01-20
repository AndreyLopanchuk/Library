from fastapi import HTTPException, status

INVALID_AUTHENTICATION_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_REFRESH_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token is missing or invalid.",
)

FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to access this resource",
)

INVALID_ACCESS_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Access token is missing or invalid.",
    headers={"WWW-Authenticate": "Bearer"},
)

PASSWORDS_MISMATCH = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The two password fields didn't match.",
)
