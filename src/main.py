from typing import Annotated
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse

from fastapi_utils.tasks import repeat_every

import bcrypt
import jwt

from . import auth
from . import models
from . import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, PREFIX, DATABASE

app = FastAPI()
api = APIRouter(prefix=PREFIX)

app.mount("/docs", StaticFiles(directory="docs"), name="docs")

@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="The root endpoint of the API",
)
async def root():
    return {
        "message": "Welcome to the API",
        "docs": "curl /docs/README.md to see the documentation",
        "helpers": "`curl https://mmo.tathya.hackclub.app/mcurl -o mcurl` to download the mcurl file."
    }

@app.get("/mcurl", response_class=FileResponse)
async def mcurl():
    return "mcurl"

@api.post(
    "/oauth2",
    response_model=models.Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": models.Error,
            "description": "Incorrect username or password"
        },
        status.HTTP_201_CREATED: {
            "model": models.Token,
            "description": "User created"
        }
    },
    tags=["auth"],
    summary="Login to get an access token",
    description=Path("docs/endpoints/post_oauth2.md").read_text(),
    response_description="The access token",
)
async def login(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
):
    with open(DATABASE, "r") as file:
        users = json.load(file)

    if username not in users:
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

        access_token = auth.create_access_token(
            data={"sub": username},
            expires=expires,
            secret=SECRET_KEY,
            algorithm=ALGORITHM
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User created",
                "data": models.Token(access_token=access_token, token_type="bearer").dict()
            }
        )

    user = users[username]
    if not auth.verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password. If you're trying to register with this username, it likely means the username is already taken."
        )

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": username},
        expires=expires,
        secret=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User logged in",
            "data": models.Token(access_token=access_token, token_type="bearer").dict()
        }
    )


@api.get("/me")
async def read_users_me(current_user: Annotated[dict, Depends(auth.get_current_user)]):
    return {"username": current_user["sub"]}

app.include_router(api)

