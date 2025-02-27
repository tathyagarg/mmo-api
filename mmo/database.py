import json
from . import models
from . import DATABASE

def get_users():
    with open(DATABASE, "r") as file:
        return json.load(file)

def update_user(player: models.Player):
    users = get_users()
    users[player.username]["data"] = player.data.model_dump()
    with open(DATABASE, "w") as file:
        json.dump(users, file)
