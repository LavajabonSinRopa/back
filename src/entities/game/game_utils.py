from ..db.gamesRepo import repo
from sqlalchemy.exc import NoResultFound
import uuid
from ..player.player_utils import drawn_figure_card, take_move_card


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


def get_players_status(game_id):
    list_status = []
    for player_id in get_game_by_id(game_id)["players"]:
        list_status.append(repo.get_player(player_id))
    return list_status


def get_game_status(game_id):
    game = get_game_by_id(game_id)
    
    if game is None:
        raise ValueError(f"No game found with ID: {game_id}")
    
    status = {
        "unique_id": game['unique_id'],
        "name": game['name'],
        "state": game['state'],
        "board": repo.get_board(game_id),
        "turn": game['turn'],
        "creator": game['creator'],
        "players": get_players_status(game_id)
    }
    return status


def get_players_names(game_id):
    list_names= []
    for player_id in get_game_by_id(game_id)["players"]:
        list_names.append(repo.get_player(player_id)["name"])
    return list_names
    
def get_games_with_player_names():
    games = get_games()
    return [
            {
            "unique_id": game['unique_id'],
            "name": game['name'],
            "state": game['state'],
            "turn": game['turn'],
            "creator": game['creator'],
            "players": game['players'],
            "player_names": get_players_names(game_id=game['unique_id'])
            }
            for game in games
        ]
  


def add_to_game(player_id,game_id):
    try:
        game = repo.get_game(game_id)

        # Verificar que no se llegó a la cantidad máxima de players
        if len(game["players"]) >= 4 or game['state'] != 'waiting':
            return -1
        
        repo.add_player_to_game(player_id=player_id,game_id=game_id)
    except Exception as e:
        raise e

def remove_player_from_game(player_id, game_id):
    try:
        repo.remove_player_from_game(player_id=player_id, game_id=game_id)
    except Exception as e:
        raise e
    
def get_players_names(game_id):
    return get_game_by_id(game_id=game_id)['player_names']

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

def create_move_deck_for_game(game_id):
    for card_type in range(7):
        for _ in range(7):
            repo.create_card(card_type=card_type, card_kind='movement', player_id=None, game_id=game_id)
    
def create_figure_cards(game_id):
    amount_players = len(get_players_status(game_id))
    amount_easy_cards = 14 // amount_players
    amount_hard_cards = 36 // amount_players
    # Crear cartas fáciles y difíciles
    easy_cards = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    hard_cards = [7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24]

    # Distribuir cartas fáciles
    for player in get_players_status(game_id):
        player_id = player['unique_id']
        for _ in range(amount_easy_cards):
            card_type = easy_cards.pop()
            repo.create_card(card_type=card_type, card_kind='figure', player_id=player_id,game_id=game_id,state='not drawn')
    # Distribuir cartas dificiles
    for player in get_players_status(game_id):
        player_id = player['unique_id']
        for _ in range(amount_hard_cards):
            card_type = hard_cards.pop()
            repo.create_card(card_type=card_type, card_kind='figure', player_id=player_id,game_id=game_id,state='not drawn')

def get_move_deck(game_id):
    return repo.get_move_deck(game_id)

def start_game_by_id(game_id):
    #TODO initialize game board
    game = get_game_by_id(game_id)
    if game["state"] == "waiting":
        repo.edit_game_state(game_id,"started")
        repo.create_board(game_id)
        create_move_deck_for_game(game_id)
        create_figure_cards(game_id)
        for player_id in game["players"]:
            for _ in range(3):
                take_move_card(player_id,game_id)
                drawn_figure_card(player_id)
    else:
        raise ValueError("Game is not in waiting state")
  
def delete_all():
    repo.tear_down()
