from enum import Enum
from ..db.gamesRepo import repo
from sqlalchemy.exc import NoResultFound
import uuid
import random
from ..player.player_utils import drawn_figure_card, take_move_card
from ..cards.movent_cards import can_move_to
from ..cards.figure_cards import figure_exists, figure_matches_type

BOARD_LEN = 6


class FigureResult(Enum):
    INVALID = 0
    COMPLETED = 1
    PLAYER_WON = 2


def add_game(game_name, creator_id, password = ""):
    new_game_id = repo.create_game(unique_id = str(uuid.uuid4()), name = game_name, state = "waiting", creator_id = creator_id, password = password)
    #Creator_id is added as player
    repo.add_player_to_game(player_id=creator_id, game_id=new_game_id,password=password)
    return new_game_id
    
def get_games():
    games = repo.get_games()
    games_waiting = [game for game in games if game['state'] == 'waiting'] 
    return games_waiting

def get_game_by_id(game_id):
    """
    Get a specific game by its unique ID.
    Args:
        game_id (str): The unique ID of the game.

    Returns:
        Game or None: The game object if found, otherwise None.
    """
    try:
        game = repo.get_game(game_id)
    except Exception as e:
        raise e
    
    return game


def get_players_status(game_id):
    list_status = []
    for player_id in get_game_by_id(game_id)["players"]:
        list_status.append(repo.get_player(player_id))
    return list_status


def get_game_status(game_id):
    game = get_game_by_id(game_id)
    
    if game is None:
        raise ValueError(f"No game found with ID: {game_id}")
    
    board = highlight_figures(game['board'])

    #resaltar casillas usadas en movimientos temporales --> % al final del color
    player_id = game['players'][game['turn']%len(game['players'])]
    moves = repo.get_player_movements(player_id=player_id)

    for move in moves:
        if board[move['from_y']][move['from_x']][-1] != '%':
            board[move['from_y']][move['from_x']] = board[move['from_y']][move['from_x']] + '%'
        if board[move['to_y']][move['to_x']][-1] != '%':
            board[move['to_y']][move['to_x']] = board[move['to_y']][move['to_x']] + '%'

    status = {
        "unique_id": game['unique_id'],
        "name": game['name'],
        "state": game['state'],
        "board": board,
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
            "type": game['type'],
            "state": game['state'],
            "turn": game['turn'],
            "creator": game['creator'],
            "players": game['players'],
            "player_names": get_players_names(game_id=game['unique_id'])
            }
            for game in games
        ]

def add_to_game(player_id,game_id, password = ""):
    try:
        game = repo.get_game(game_id)

        # Verificar que no se llegó a la cantidad máxima de players
        if len(game["players"]) >= 4 or game['state'] != 'waiting':
            return -1
        
        repo.add_player_to_game(player_id=player_id,game_id=game_id, password = password)
    except Exception as e:
        raise e

def remove_player_from_game(player_id, game_id):
    try:
        repo.remove_player_from_game(player_id=player_id, game_id=game_id)
        remove_all_movements(player_id=player_id,game_id=game_id)
    except Exception as e:
        raise e
    
def get_players_names(game_id):
    return get_game_by_id(game_id=game_id)['player_names']

def is_players_turn(game_id, player_id):
    try:
        game = get_game_by_id(game_id=game_id)
    except Exception as e:
        raise e
    return game['players'][game['turn']%len(game['players'])]==player_id

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
    
    try:

        if(player_id not in game['players']):
            return False

        if(game['players'][game['turn']%len(game['players'])]!=player_id):
            return False

        movements = repo.get_player_movements(player_id=player_id)

        for movement in movements:
            remove_top_movement(game_id=game_id, player_id=player_id)

        n = len(repo.get_player(player_id=player_id)['movement_cards'])
        while n<3:
            take_move_card(player_id,game_id)
            n+=1
        
        cards_in_hand = repo.get_player(player_id=player_id)['figure_cards']
        is_blocked = False
        for card in cards_in_hand:
            if card['state'] == 'blocked':
                is_blocked = True
        n = len(cards_in_hand)
        while n<3 and not is_blocked:
            drawn_figure_card(player_id)
            n+=1

        repo.pass_turn(game_id=game_id)

        return True
    except Exception as e:
        print(e)
        raise e

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

    random.shuffle(hard_cards)
    random.shuffle(easy_cards)

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

def is_in_board(x):
    #TODO make global variable for board size
    return x >= 0 and x < BOARD_LEN

def make_temp_movement(game_id, player_id, card_id, from_x, from_y, to_x, to_y):
    # assumes that player is in game
    # check if player has a card of this type and movement can be made using card given
    # call repo.add_movement()
    # return true if movement successful, false or exception if not
    
    if not is_in_board(from_x) or not is_in_board(from_y) or not is_in_board(to_x) or not is_in_board(to_y):
        raise Exception("403, INCORRECT COORDINATES")

    try :
        player = repo.get_player(player_id=player_id)
        cards = player['movement_cards']
        card_type = -1
    
        for card in cards:
            if card['unique_id'] == card_id:
                card_type = card['type']
    
        if card_type==-1:
            raise Exception("403, player does not have THIS card")
    
        if(can_move_to(from_x=from_x, from_y=from_y, to_x=to_x, to_y=to_y, card_type=card_type)):
            repo.add_movement(player_id=player_id, from_x=from_x, from_y=from_y, to_x=to_x, to_y=to_y, card_id=card_id)
            repo.swap_positions_board(game_id=game_id, x1 = from_x, y1 = from_y, x2 = to_x, y2 = to_y)
            return True
        return False
    
    except Exception as e:
        raise e


directions = [[0,1],[0,-1],[1,0],[-1,0]]

def highlight_figures(board: list[list[str]]) -> list[list[str]]:
    n = len(board)
    vis = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if(vis[i][j]):
                continue
            vis[i][j] = True
            processing = [[i,j]]
            figure = [[i,j]]
            color = board[i][j]
            while(len(processing)>0):
                square = processing[-1]
                processing.pop()
                x,y = square[0],square[1]
                for d in directions:
                    nx,ny = x + d[0], y + d[1]
                    if not is_in_board(nx) or not is_in_board(ny):
                        continue
                    if not vis[nx][ny] and board[nx][ny] == color:
                        vis[nx][ny] = True
                        processing.append([nx,ny])
                        figure.append([nx,ny])
            if figure_exists(figure):
                for square in figure:
                    board[square[0]][square[1]] = board[square[0]][square[1]].upper()
    return board


def remove_top_movement(game_id, player_id):
    try:
        game = repo.get_game(game_id)
        movements = repo.get_player_movements(player_id=player_id)
        if not movements:
            raise Exception("403, player has no movements")
        repo.swap_positions_board(game_id=game_id, x1 = movements[-1]['from_x'], y1 = movements[-1]['from_y'], x2 = movements[-1]['to_x'], y2 = movements[-1]['to_y'])
        repo.remove_top_movement(player_id=player_id)
    except Exception as e:
        raise e
    
def apply_temp_movements(player_id):
    repo.apply_temp_movements(player_id=player_id)

# cancels all temp moves made so far
def remove_all_movements(game_id, player_id):
    while(len(repo.get_player_movements(player_id=player_id))>0):
        remove_top_movement(game_id=game_id,player_id=player_id)

def get_figure(board, i, j):
    vis = [[False]*BOARD_LEN for _ in range(BOARD_LEN)]
    vis[i][j] = True
    processing = [[i,j]]
    figure = [[i,j]]
    color = board[i][j]
    while(len(processing)>0):
        square = processing[-1]
        processing.pop()
        x,y = square[0],square[1]
        for d in directions:
            nx,ny = x + d[0], y + d[1]
            if not is_in_board(nx) or not is_in_board(ny):
                continue
            if not vis[nx][ny] and board[nx][ny] == color:
                vis[nx][ny] = True
                processing.append([nx,ny])
                figure.append([nx,ny])
    return figure

def complete_figure(game_id, player_id, card_id, i, j):

    try:
        game = repo.get_game(game_id)
        if player_id not in game['players']:
            raise Exception("Not in game")
        if not is_players_turn(game_id=game_id, player_id=player_id):
            raise Exception("Not your turn")
        
        card_type = -1
        cards = repo.get_player(player_id=player_id)['figure_cards']
        for card in cards:
            if card['unique_id'] == card_id:
                card_type = card['type']
                if card['state'] == 'blocked':
                    raise Exception("This card is already blocked!")
        if card_type == -1:
            raise Exception("Doesn't have card")

        board = game['board']
        figure = get_figure(board=board, i = i, j = j)

        #TODO: check color prohibido 
        if not figure_matches_type(figure_type=card_type, figure=figure):
            raise Exception("Figure doesn't match")

        apply_temp_movements(player_id=player_id)
        # discard figure card
        repo.discard_card(card_id=card_id)

        #TODO: update color prohibido

        # Check if player ran out of cards after discarding
        player_cards = repo.get_player_figure_cards(player_id=player_id)['figure_cards']
        remaining_cards = len([fcard for fcard in player_cards if fcard["state"] != "discarded"])

        if remaining_cards <= 0:
            return FigureResult.PLAYER_WON
            
        cards_in_hand = repo.get_player(player_id=player_id)['figure_cards']
        if(len(cards_in_hand)==1):
            repo.unblock_card(card_id=cards_in_hand[0]['unique_id'])
        return FigureResult.COMPLETED

    except Exception as e:
        raise e

def block_figure(game_id, player_id, card_id, i, j):

    try:
        game = repo.get_game(game_id)
        if player_id not in game['players']:
            raise Exception("Not in game")
        if not is_players_turn(game_id=game_id, player_id=player_id):
            raise Exception("Not your turn")
        
        card_type = -1
        owner_blocked = False
        for player in repo.get_game(game_id=game_id)['players']:
            if(player_id==player):
                continue
            player_cards = repo.get_player(player_id=player)['figure_cards']
            print(player_cards)
            for card in player_cards:
                if card['unique_id'] == card_id:
                    card_type = card['type']
                    if card['state'] == 'blocked':
                        raise Exception("Card is already blocked")
                if card['state']== 'blocked':
                    owner_blocked = True
        
        if card_type == -1:
            raise Exception("Card non existent")

        if owner_blocked:
            raise Exception("Owner of the card has a blocked card already")

        board = game['board']
        
        figure = get_figure(board=board, i = i, j = j)

        #TODO: check color prohibido
        if not figure_matches_type(figure_type=card_type, figure=figure):
            raise Exception("Figure doesn't match")
        
        apply_temp_movements(player_id=player_id)

        # block figure card
        repo.block_card(card_id=card_id)

        #TODO: update color prohibido
        return True

    except Exception as e:
        raise e

def delete_all():
    repo.tear_down()

