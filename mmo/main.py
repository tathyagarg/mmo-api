from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from . import auth, game
from . import PREFIX

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
        "docs": "curl https://mmo.tathya.hackclub.app/docs/README.md to see the documentation",
        "helpers": "`curl https://mmo.tathya.hackclub.app/mcurl -o mcurl` to download the mcurl file."
    }


@app.get("/mcurl", response_class=FileResponse)
async def mcurl():
    return "mcurl"


api.include_router(auth.auth_router)
api.include_router(game.player_router)
app.include_router(api)

