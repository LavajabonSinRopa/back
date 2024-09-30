from ..db.gamesRepo import repo
import uuid

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
    repo.add_player_to_game(player_id=player_id,game_id=game_id)

def delete_all():
    repo.tear_down()
    
def get_players_names(game_id):
    list_names= []
    for player_id in get_game_by_id(game_id)["players"]:
        list_names.append(repo.get_player(player_id)["name"])
    return list_names