import datetime
from datetime import timedelta
from typing import Annotated
from pathlib import Path
import json

from fastapi import Depends, Body, status, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

import jwt
import bcrypt

from . import PREFIX, SECRET_KEY, ALGORITHM, DATABASE, ACCESS_TOKEN_EXPIRE_MINUTES, RESERVED_USERNAMES
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/auth/login")
auth_router = APIRouter(prefix=f"/auth", tags=["auth"])
 
ERROR_RESPONSES: dict[int, dict[str, str]] = {
    status.HTTP_410_GONE: {"description": "Token has expired"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
}

def verify_password(plain: str, hashed: str):
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict, expires: timedelta, secret: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + expires
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret, algorithm=algorithm)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict | int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        exp = datetime.datetime.fromtimestamp(payload.get('exp', 0), tz=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.UTC)

        if now >= exp:
            raise jwt.ExpiredSignatureError

        return payload
    except jwt.ExpiredSignatureError:
        return status.HTTP_410_GONE
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED


def make_error_invalid_user(status_code: int) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ERROR_RESPONSES.get(status_code, {"description": "Unknown error"})["description"]
    )


async def authentication_required(request: Request) -> models.Player:
    token = await oauth2_scheme(request)
    if not token:
        raise make_error_invalid_user(status.HTTP_401_UNAUTHORIZED)

    current_user = get_current_user(token)
    if isinstance(current_user, int):
        raise make_error_invalid_user(current_user)

    with open(DATABASE, "r") as file:
        users = json.load(file)

    if current_user["sub"] not in users:
        raise make_error_invalid_user(status.HTTP_401_UNAUTHORIZED)

    player = models.Player(username=current_user["sub"], data=users[current_user["sub"]]["data"])

    return player


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
    request: Request
):
    with open(DATABASE, "r") as file:
        users = json.load(file)

    if username in users or (username in RESERVED_USERNAMES and not request.headers.get("Is-Testing")):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is taken"
        )

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    users[username] = {
        "password": hashed_password.decode(),
        "salt": salt.decode(),
        "data": models.PlayerData(x=0, y=0).model_dump()
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
    request: Request
):
    with open(DATABASE, "r") as file:
        users = json.load(file)

    user = users.get(username)
    if user is None or (username in RESERVED_USERNAMES and not request.headers.get("Is-Testing")):
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

@auth_router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    tags=["auth"],
    summary="Delete a user",
    description=Path("docs/endpoints/auth/delete_delete.md").read_text(),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password"
        },
    },
)
async def delete_user(
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

    del users[username]

    with open(DATABASE, "w") as file:
        json.dump(users, file, indent=4)

    return {
        "message": "User deleted"
    } 
