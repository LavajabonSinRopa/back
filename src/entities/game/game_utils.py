from ..game.game import Game

games = {}
#adds a game to the games dictionary
#TODO: database functionality
def add_game(new_game):
    if(not new_game.unique_id in games):
        games[new_game.unique_id] = new_game

def print_game(game):
    print(game.name + '\n' + game.unique_id)

def get_games():
    return games

def get_game_by_id(game_id):
    """
    Get a specific game by its unique ID.
    Args:
        game_id (str): The unique ID of the game.

    Returns:
        Game or None: The game object if found, otherwise None.
    """
    return games.get(game_id)

#temp func until we have BD
def get_listed_games():
    game_list = []
    for game in games:
        game_list.append({"name": games[game].name, "players": len(games[game].players), "state": games[game].state,"id": games[game].unique_id})
    return game_list