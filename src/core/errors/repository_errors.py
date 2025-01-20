from fastapi import HTTPException, status

OBJECT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Object not found",
)

RESOURCE_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Resource already exists",
)
