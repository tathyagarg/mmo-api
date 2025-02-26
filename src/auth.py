from datetime import datetime, timedelta
from typing import Annotated
from pathlib import Path
import json

from fastapi import Depends, Body, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

import jwt
import bcrypt

from . import PREFIX, SECRET_KEY, ALGORITHM, DATABASE, ACCESS_TOKEN_EXPIRE_MINUTES
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/auth/login")
auth_router = APIRouter(prefix=f"/auth", tags=["auth"])
 

def verify_password(plain: str, hashed: str):
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict, expires: timedelta, secret: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret, algorithm=algorithm)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict | int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if datetime.fromtimestamp(payload.get('exp', 0)) < datetime.utcnow():
            raise jwt.ExpiredSignatureError

        return payload
    except jwt.ExpiredSignatureError:
        return stauts.HTTP_410_GONE
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED


@auth_router.post(
    "/signup",
    response_model=models.LoginSuccessful,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
    summary="Signup and get an access token",
    description=Path("docs/endpoints/auth/post_signup.md").read_text(),
    response_description="The access token",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Username is taken"
        },
    },
)
async def signup(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
):
    with open(DATABASE, "r") as file:
        users = json.load(file)

    if username in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is taken"
        )

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    users[username] = {
        "password": hashed_password.decode(),
        "salt": salt.decode(),
        "data": {}
    }

    with open(DATABASE, "w") as file:
        json.dump(users, file, indent=4)

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": username},
        expires=expires,
        secret=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=models.LoginSuccessful(
            message="User created",
            data=models.Token(access_token=access_token, token_type="bearer")
        ).model_dump()
    )


@auth_router.get(
    "/login",
    response_model=models.LoginSuccessful,
    status_code=status.HTTP_200_OK,
    tags=["auth"],
    summary="Login to get an access token",
    description=Path("docs/endpoints/auth/get_login.md").read_text(),
    response_description="The access token",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found"
        },
    },
)
async def login(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
):
    with open(DATABASE, "r") as file:
        users = json.load(file)

    user = users.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username},
        expires=expires,
        secret=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=models.LoginSuccessful(
            message="User logged in",
            data=models.Token(access_token=access_token, token_type="bearer")
        ).model_dump()
    )
