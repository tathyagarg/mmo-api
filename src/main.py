from typing import Annotated
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
import jwt
import dotenv

import auth
import models

success = dotenv.load_dotenv()
if not success:
    raise Exception("Failed to load .env file")

DATABASE = "data/users.json"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

PREFIX = "/api/v1"

app = FastAPI()
api = APIRouter(prefix=PREFIX)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{PREFIX}/token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@api.post(
    "/token",
    response_model=models.Token,
    responses={
        401: {"model": models.Error}
    },
    tags=["token"],
    summary="Login to get an access token",
    description=Path("docs/post_token.md").read_text(),
    response_description="The access token",
)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password

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

        return models.Token(access_token=access_token, token_type="bearer")

    user = users[username]
    if not auth.verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": username},
        expires=expires,
        secret=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return models.Token(access_token=access_token, token_type="bearer")


@api.get("/me")
async def read_users_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"username": current_user["sub"]}

app.include_router(api)

