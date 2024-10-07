from ..db.gamesRepo import repo
from sqlalchemy.exc import NoResultFound
import uuid
from ..player import player_utils


def add_game(game_name, creator_id):
    new_game_id = repo.create_game(unique_id = str(uuid.uuid4()), name = game_name, state = "waiting", creator_id = creator_id)
    #Creator_id is added as player
    repo.add_player_to_game(player_id=creator_id, game_id=new_game_id)
    return new_game_id
    
def get_games():
    return repo.get_games()

def get_game_by_id(game_id):
    """
    Get a specific game by its unique ID.
    Args:
        game_id (str): The unique ID of the game.

    Returns:
        Game or None: The game object if found, otherwise None.
    """
    return repo.get_game(game_id)

def add_to_game(player_id,game_id):
    try:
        game = repo.get_game(game_id)

        # Verificar que no se llegó a la cantidad máxima de players
        if len(game["players"]) >= 4:
            return -1
        
        repo.add_player_to_game(player_id=player_id,game_id=game_id)
    except Exception as e:
        raise e

def remove_player_from_game(player_id, game_id):
    try:
        repo.remove_player_from_game(player_id=player_id, game_id=game_id)
    except Exception as e:
        raise e

def delete_all():
    repo.tear_down()
    
def get_players_names(game_id):
    list_names= []
    for player_id in get_game_by_id(game_id)["players"]:
        list_names.append(repo.get_player(player_id)["name"])
    return list_names

def pass_turn(game_id, player_id):
    """
    passes turn if it is player_id's turn and broadcasts to players in game if successful 
    Args: 
        game_id (str): The unique ID of the game.
        player_id(str): The unique ID of the player
    
    Returns:
        bool: true if the turn could be passed, false otherwise
    """
    try:
        game = get_game_by_id(game_id=game_id)
    except Exception as e:
        raise e
    
    if(player_id not in game['players']):
        return False
    
    if(game['players'][game['turn']%len(game['players'])]!=player_id):
        return False
    
    repo.pass_turn(game_id=game_id)
    return True

def get_players_status(game_id):
    list_status = []
    for player_id in get_game_by_id(game_id)["players"]:
        list_status.append(repo.get_player(player_id))
    return list_status

def start_game_by_id(game_id):
    #TODO initialize game board
    game = get_game_by_id(game_id)
    if game["state"] == "waiting":
        repo.edit_game_state(game_id,"started")
        for player_id in game["players"]:
            player_utils.take_move_card(game_id,player_id)
            player_utils.take_figures_card(game_id,player_id)
    else:
        raise ValueError("Game is not in waiting state")
    
