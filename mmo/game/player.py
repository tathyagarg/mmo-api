from typing import Annotated

from fastapi import APIRouter, Depends

from .. import auth
from .. import PREFIX

player_router = APIRouter(prefix=f"{PREFIX}/player", tags=["player"])

@player_router.get(
    "/me"
)
@auth.authentication_required
async def get_current_user(current_user: Annotated[dict, Depends(auth.get_current_user)]):
    return {"username": current_user["sub"]}
