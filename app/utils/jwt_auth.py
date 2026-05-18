from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

# from database.session import get_db, SessionLocal
from config import settings

SECRET_KEY = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


class JWTUtils:
    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

    @classmethod
    def get_tokens_with_refresh(
        cls, data: dict, expires_delta: Optional[timedelta] = None
    ):

        return {
            "access_token": cls.create_access_token(
                data=data, expires_delta=expires_delta
            ),
            "refresh_token": cls.create_refresh_token(
                data=data, expires_delta=expires_delta
            ),
        }


class CustomAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        try:
            payload = JWTUtils.decode_token(credentials.credentials)
            request.state.user_payload = payload  # Optional: store in request.state
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
