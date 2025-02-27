from typing import Annotated

from fastapi import APIRouter, Depends

from .. import auth, models

player_router = APIRouter(prefix="/player", tags=["player"])

@player_router.get(
    "/me"
)
async def read_user(player: Annotated[models.Player, Depends(auth.authentication_required)]):
    return player.model_dump()
