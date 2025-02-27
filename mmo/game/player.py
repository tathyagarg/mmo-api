from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from .. import auth, models, database

player_router = APIRouter(prefix="/player", tags=["player"])

DIRECTIONS = {
    "north": (0, 1),
    "south": (0, -1),
    "east": (1, 0),
    "west": (-1, 0),
}

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


@player_router.put(
    "/move/{direction}",
    response_model=models.Player,
    summary="Move the player",
    description=Path("docs/endpoints/player/put_move_direction.md").read_text(),
    response_description="The current player",
    responses={
        **auth.ERROR_RESPONSES,
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid direction"
        }
    },
)
async def move_player(
    player: Annotated[models.Player, Depends(auth.authentication_required)],
    direction: str
):
    direction = direction.lower()

    if direction not in DIRECTIONS:
        raise HTTPException(status_code=400, detail="Invalid direction")

    x, y = DIRECTIONS[direction]

    player.data.x += x
    player.data.y += y

    database.update_user(player)

    return player.model_dump()

