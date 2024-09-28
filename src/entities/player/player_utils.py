from ..db.gamesRepo import repo
from ..db.models import Player
import uuid

def add_player(player_name):
    new_player_id = repo.create_player(unique_id = str(uuid.uuid4()), name=player_name)
    return new_player_id