# JWT 문자열을 인코딩, 디코딩 하는 함수가 포함.
import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError
from planner.database.connection import Settings

settings = Settings()

import logging

logger = logging.getLogger("users")
logger.setLevel(logging.DEBUG)


def create_access_token(user: str):
    payload = {"user": user, "expires": time.time() + 3600}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    # payload정보, 사인할 키, 사인 및 암호화 알고리즘(기본값인 HS256이 가장 많이 사용됨)
    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )

        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
