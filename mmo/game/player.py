from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Depends

from .. import auth, models

player_router = APIRouter(prefix="/player", tags=["player"])

@player_router.get(
    "/me",
    response_model=models.Player,
    summary="Get the current player",
    description=Path("docs/endpoints/player/get_me.md").read_text(),
    response_description="The current player",
    responses={
        **auth.ERROR_RESPONSES,
    },
)
async def read_user(player: Annotated[models.Player, Depends(auth.authentication_required)]):
    return player.model_dump()
