# authenticate 의존 라이브러리가 포함되며, 인증 및 권한을 위해 라우트에 주입됨.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from planner.auth.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)
    return decoded_token["user"]
