from entities.game.game import Game

games = {}

#adds a game to the games dictionary
#TODO: database functionality
def add_game(new_game):
    games[new_game.unique_id] = new_game

def print_game(game):
    print(game.name + '\n' + game.unique_id)

def get_games():
    return games