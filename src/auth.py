from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import jwt
import bcrypt

from . import PREFIX, SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/oauth2")
 
def verify_password(plain: str, hashed: str):
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(data: dict, expires: timedelta, secret: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret, algorithm=algorithm)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

