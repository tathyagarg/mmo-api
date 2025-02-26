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


@api.get("/me")
async def read_users_me(current_user: Annotated[dict, Depends(auth.get_current_user)]):
    if isinstance(current_user, int):
        if current_user == status.HTTP_410_GONE:
            raise HTTPException(
                status_code=current_user,
                detail="Token has expired"
            )
        elif current_user == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=current_user,
                detail="Invalid token"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown error"
            )

    return {"username": current_user["sub"]}

api.include_router(auth.auth_router)
app.include_router(api)

