import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from database.connection import Settings

settings = Settings()

def create_access_token(user: str):
    payload = {
        'user': user,
        'expires': datetime.utcnow() + settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire = data.get('expires')

        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token expired')

        return data

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')