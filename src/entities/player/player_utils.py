from ..db.gamesRepo import repo
from ..db.models import Player
import uuid
import random

AMOUNT_FIGURE_FOR_PLAYER = 3

def add_player(player_name):
    new_player_id = repo.create_player(unique_id = str(uuid.uuid4()), name=player_name)
    return new_player_id

def take_move_card(game_id,player_id):
    card_info = repo.create_card(random.randint(0,6),"movement",player_id,game_id)
    return card_info
    

def take_figures_card(game_id,player_id):
    card_info = []
    for i in range(AMOUNT_FIGURE_FOR_PLAYER):
               card_info.append(repo.create_card(random.randint(0, 12), "figure", player_id, game_id, "Drawn"))

    return card_info