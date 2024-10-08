from ..db.gamesRepo import repo
import uuid

def add_player(player_name):
    new_player_id = repo.create_player(unique_id = str(uuid.uuid4()), name=player_name)
    return new_player_id

def take_move_card(player_id,game_id):
    repo.take_move_card(player_id,game_id)

def drawn_figure_card(player_id):
    repo.drawn_figure_card(player_id)