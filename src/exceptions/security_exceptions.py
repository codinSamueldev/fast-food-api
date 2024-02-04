from fastapi import HTTPException
from starlette import status

CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user : (", headers={"WWW-Authenticate": "Bearer"})
