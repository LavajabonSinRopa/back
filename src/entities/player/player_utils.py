from ..db.gamesRepo import repo
from ..db.models import Player
import uuid
import random

AMOUNT_FIGURE_FOR_PLAYER = 3

def add_player(player_name):
    new_player_id = repo.create_player(unique_id = str(uuid.uuid4()), name=player_name)
    return new_player_id

def take_move_card(game_id,player_id):
    card_info = repo.create_card(card_type=random.randint(0,6),card_kind="movement",player_id=player_id,game_id=game_id)
    return card_info
    

def take_figures_card(game_id,player_id):
    card_info = []
    for i in range(AMOUNT_FIGURE_FOR_PLAYER):
               card_info.append(repo.create_card(card_type=random.randint(0, 12), card_kind="figure",player_id=player_id, game_id=game_id, state="Drawn"))

    return card_info