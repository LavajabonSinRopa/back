from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from .models import Game, Player, engine, Figure_card, Movement_card, Movement
from typing import List
import uuid
import random

# Create a session
Session = sessionmaker(bind=engine)

class gameRepository:
    @staticmethod
    def create_game(unique_id: str,name: str, state: str, creator_id: str) -> Game:
        session = Session()
        try:
            new_game = Game(unique_id = unique_id, name=name, state=state, creator=creator_id, turn=0)
            session.add(new_game)
            session.commit()
            return new_game.unique_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def create_player(name: str, unique_id: str) -> Player:
        session = Session()
        try:
            new_player = Player(unique_id=unique_id, name=name)
            session.add(new_player)
            session.commit()
            return new_player.unique_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_game(game_id: str) -> dict:
        session = Session()
        try:
            game = session.query(Game).filter_by(unique_id=game_id).one()
            return {
                "unique_id": game.unique_id,
                "name": game.name,  
                "state": game.state,
                "turn": game.turn,
                "creator": game.creator,
                "players": [player.unique_id for player in game.players],
                "player_names": [player.name for player in game.players],
                "board": gameRepository.get_board(game_id)
            }
        except NoResultFound:
            raise ValueError("Game_model does not exist")
        finally:
            session.close()

    @staticmethod
    def get_player(player_id: str) -> dict:
        session = Session()
        try:
            player = session.query(Player).filter_by(unique_id=player_id).one()
            return {
                "unique_id": player.unique_id,
                "name": player.name,
                "figure_cards": [{'type': fcard.card_type, 'unique_id': fcard.unique_id, 'state': fcard.state} for fcard in player.figure_cards if not fcard.state == 'not drawn' and not fcard.state == 'discarded'],
                "movement_cards": [{'type': mcard.card_type, 'unique_id': mcard.unique_id, 'state': mcard.state} for mcard in player.movement_cards]
            }
        except NoResultFound:
            raise ValueError("Game_model does not exist")
        finally:
            session.close()

    @staticmethod
    def get_player_figure_cards(player_id : str) -> dict:
        session = Session()
        try:
            player = session.query(Player).filter_by(unique_id=player_id).one()
            return {
                "figure_cards": [{'type': fcard.card_type, 'unique_id': fcard.unique_id, 'state': fcard.state} for fcard in player.figure_cards]
            }
        except NoResultFound:
            raise ValueError("Game_model does not exist")
        finally:
            session.close()

    @staticmethod
    def get_games() -> List[dict]:
        session = Session()
        try:
            games = session.query(Game).all()
            return [
                {
                    "unique_id": game.unique_id,
                    "name": game.name,
                    "state": game.state,
                    "turn": game.turn,
                    "creator": game.creator,
                    "players": [player.unique_id for player in game.players],
                    "player_names": [player.name for player in game.players]
                }
                for game in games
            ]
        finally:
            session.close()
   
    @staticmethod
    def tear_down():
        session = Session()
        try:
            # Delete all entries from the Players table
            session.query(Player).delete()
            # Delete all entries from the Games table
            session.query(Game).delete()
            # Deleete all entries from the Cards table
            session.query(Figure_card).delete()
            session.query(Movement_card).delete()
            # Commit the changes
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add_player_to_game(player_id: str, game_id: str):
        session = Session()
        try:
            # Retrieve the player and game
            player = session.query(Player).filter_by(unique_id=player_id).one()
            game = session.query(Game).filter_by(unique_id=game_id).one()
            
            # Add the player to the game
            if player not in game.players:
                game.players.append(player)
                session.commit()
            else:
                print(f"Player {player_id} is already in game {game_id}.")
        except NoResultFound:
            raise ValueError("Player or Game does not exist")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def create_card(card_type, card_kind, player_id, game_id, state=None):
        """
        Creates a card of a specific type and assigns it to a player.

        :param card_type: The type of the card (Integer).
        :param card_kind: 'figure' for Figure_card or 'movement' for Movement_card.
        :param player_id: The unique ID of the player.
        :param game_id: The unique ID of the game.
        :param state: The state of the card (only applicable for Figure_card).
        """
        # Start a new session
        session = Session()
        try:
            
            player = session.query(Player).filter_by(unique_id=player_id).one_or_none()
            
            # Instantiate the card based on the specified class
            if card_kind == 'figure':
                card = Figure_card(unique_id=str(uuid.uuid4()), card_type=card_type, state=state, player_id=player_id, game_id=game_id)
                if player != None:
                    player.figure_cards.append(card)
                else:
                    session.add(card)
            elif card_kind == 'movement':
                card = Movement_card(unique_id=str(uuid.uuid4()), card_type=card_type, player_id=player_id, game_id=game_id)
                if player != None:
                    player.movement_cards.append(card)
                else:
                    session.add(card)
            else:
                raise ValueError("Invalid card class specified.")
            
            session.commit()
            return({"card_id" : card.unique_id,
                    "card_kind":card_kind,
                    "card_type":card_type,
                    "state":state})

        except Exception as e:
            session.rollback()
            print(f"Error creating card: {e}")

        finally:
            session.close()

# Example usage:
# create_card(card_type=1, card_kind='figure', player_id='player123', game_id='game456', state='Drawn')

    @staticmethod
    def get_card(card_id: str):
        session = Session()
        try:
            card = session.query(Figure_card).filter_by(unique_id=card_id).one_or_none()
            if card is None:
                card = session.query(Movement_card).filter_by(unique_id=card_id).one()
            return {
                "unique_id": card.unique_id,
                "card_type": card.card_type,
                "player_id": card.player_id,
                "game_id": card.game_id,
                "state": card.state
            }
        except NoResultFound:
            raise ValueError("Card does not exist")
        finally:
            session.close()


    @staticmethod
    def remove_player_from_game(player_id: str, game_id: str):
        session = Session()
        try:
            # Retrieve the player and game
            player = session.query(Player).filter_by(unique_id=player_id).one()
            game = session.query(Game).filter_by(unique_id=game_id).one()
            
            # Remove the player from the game
            if player in game.players:
                game.players.remove(player)
                session.commit()
            else:
                print(f"Player {player_id} is not in game {game_id}.")

            print(f"ALL PLAYERS IN ID {game_id} are {[player.name for player in game.players]}") # TO BE REMOVED
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def pass_turn(game_id: str):
        session = Session()
        try :
            game = session.query(Game).filter_by(unique_id=game_id).one()            
            game.turn += 1
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    @staticmethod
    def edit_game_state(game_id: str, new_state: str):
        session = Session()
        try:
            game = session.query(Game).filter_by(unique_id=game_id).one()
            game.state = new_state
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

## Cards
    @staticmethod
    def get_move_deck(game_id:str) -> List[dict]:
        session = Session()
        try:
            movement_cards = session.query(Movement_card).filter_by(game_id=game_id,player_id=None).all()
            return [
                {
                    'unique_id':mcard.unique_id,
                    'card_type':mcard.card_type,
                    'player_id':mcard.player_id
                 } 
                for mcard in movement_cards
            ]
        finally:
            session.close()
            
    @staticmethod
    def take_move_card(player_id:str, game_id: str):
        session = Session()
        try:
            # Retrieve the game
            game = session.query(Game).filter_by(unique_id=game_id).one_or_none()
            if game is None:
                raise ValueError(f"No game found with ID: {game_id}")

            # Retrieve the player
            player = session.query(Player).filter_by(unique_id=player_id).one_or_none()
            if player is None:
                raise ValueError(f"No player found with ID: {player_id}")

            # Retrieve the movement cards
            movement_cards = session.query(Movement_card).filter_by(player_id=None, game_id=game_id).all()
            if len(movement_cards) == 0:
                raise ValueError("No available movement cards")

            # Assign a random movement card to the player
            card = random.choice(movement_cards)
            card.player_id = player_id
            player.movement_cards.append(card)
            session.commit()
            return card.card_type
        except Exception as e:
            session.rollback()
            print(f"Error taking random movement card: {e}")
        finally:
            session.close()
    
    @staticmethod
    def drawn_figure_card(player_id:str):
        session = Session()
        try:
            # Retrieve the player
            player = session.query(Player).filter_by(unique_id=player_id).one_or_none()
            if player is None:
                raise ValueError(f"No player found with ID: {player_id}")

            if len(player.figure_cards) == 0:
                raise ValueError("No figure cards")
            for card in player.figure_cards:
                if card.state == 'not drawn':
                    card.state = 'drawn'
                    session.commit()
                    return card.card_type
        
            raise ValueError("No 'Not drawn' figure cards found") 
        except Exception as e:
            session.rollback()
            print(f"Error drawing figure card: {e}")
        finally:
            session.close()
    
    @staticmethod
    def create_board(game_id: str):
        session = Session()
        game = session.query(Game).filter_by(unique_id=game_id).one_or_none()
        
        colors = ['red', 'green', 'blue', 'yellow']
        
        color_pool = colors * 9 
        random.shuffle(color_pool)
        try:
            if game is None:
                raise ValueError(f"No game found with ID: {game_id}")
            
            board_colors = []
            for _ in range(6):
                for _ in range(6):
                    color = color_pool.pop()
                    board_colors.append(color)
            board_string = ' '.join(board_colors)
            game.board = board_string      
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating board: {e}")
        finally:
            session.close()
            
    @staticmethod
    def get_board(game_id:str) -> List[List[str]]:
        """
        Return the board matrix for a game.
        :param game_id: The unique ID of the game.
        
        board_matrix: A 6x6 matrix representing the board. Each cell contains string color. (red, green, blue, yellow)
        
        board_matrix[y][x] represents the color of the cell at position (x, y).
        """
        session = Session()
        
        board_matrix = None
        try:
            game = session.query(Game).filter_by(unique_id=game_id).one_or_none()
            if game is None:
                raise ValueError(f"No game found with ID: {game_id}")
            
            if game.board is not None:
                board_string = game.board
                board_list = board_string.split(' ')
            
                board_matrix = [[None for _ in range(6)] for _ in range(6)]
                for y in range(6):
                    for x in range(6):
                        board_matrix[y][x] = board_list.pop(0)
            return board_matrix
        except Exception as e:
            print(f"Error getting board: {e}")
        finally:
            session.close()
    
    @staticmethod
    def swap_positions_board(game_id: str, x1: int, y1: int, x2: int, y2: int):
        session = Session()
        try:
            if x1 < 0 or x1 > 5 or y1 < 0 or y1 > 5 or x2 < 0 or x2 > 5 or y2 < 0 or y2 > 5:
                raise ValueError("Invalid coordinates")
            
            game = session.query(Game).filter_by(unique_id=game_id).one_or_none()
            if game is None:
                raise ValueError(f"No game found with ID: {game_id}")
            if game.state != 'started':
                raise ValueError("Game is not started")
            
            board_list = game.board.split(' ')
            index1 = y1 * 6 + x1
            index2 = y2 * 6 + x2
            temp_color = board_list[index1]
            board_list[index1] = board_list[index2]
            board_list[index2] = temp_color
            board_string = ' '.join(board_list)
            game.board = board_string            
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error swapping positions in board: {e}")
        finally:
            session.close()
            
    @staticmethod
    def add_movement(player_id: str, card_id: str, from_x: int, from_y: int, to_x: int, to_y: int):
        # open session
        # encontrar el id del jugador a traves de la carta --> card_id && player_id
        # fijarme cuantos movientos hay --> move_number
        # crear movement
        # meter en base de datos
        # return numero de movimiento
        session = Session()
        try:
            card = session.query(Movement_card).filter_by(unique_id=card_id).one()
            if card.state == 'blocked':
                raise Exception("Error CARD ALREADY USED")
            player = session.query(Player).filter_by(unique_id=player_id).one()
            move_number = len(player.movements)
            move_id = str(uuid.uuid4())
            if(move_number>=3):
                raise Exception("Error TOO MANY MOVES")
            new_movement = Movement(unique_id = move_id, player_id = player.unique_id, from_x = from_x, from_y = from_y, to_x = to_x, to_y = to_y, card_id = card_id, move_number = move_number)
            player.movements.append(new_movement)
            card.state = 'blocked'
            session.add(new_movement)
            session.commit()
            card = session.query(Movement_card).filter_by(unique_id=card_id).one()
            return move_number
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod

    def remove_top_movement(player_id: str):
        session = Session()
        try:
            player = session.query(Player).filter_by(unique_id=player_id).one()
            if len(player.movements) == 0:
                raise ValueError("No movements to remove")
            movement = player.movements.pop()
            card = session.query(Movement_card).filter_by(unique_id=movement.card_id).one()
            card.state = 'not blocked'
            session.delete(movement)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error removing top movement: {e}")
        finally:
            session.close()


    @staticmethod
    def apply_temp_movements(player_id: str):
        session = Session()
        try:
            player = session.query(Player).filter_by(unique_id=player_id).one()
            player_movements = player.movements
            for movement in player_movements:
                card = session.query(Movement_card).filter_by(unique_id=movement.card_id).one()
                card.state = 'not drawn'
                card.player_id = None
                session.delete(movement)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error applying temps movements: {e}")
        finally:
            session.close()

    @staticmethod
    def get_player_movements(player_id: str) -> dict:
        session = Session()
        try:
            player = session.query(Player).filter_by(unique_id=player_id).one()
            return [{'from_x' : m.from_x, 'from_y' : m.from_y, 'to_x' : m.to_x, 'to_y' : m.to_y} for m in player.movements]
        except NoResultFound:
            raise ValueError("Game_model does not exist")
        finally:
            session.close()

    @staticmethod
    def discard_card(card_id: str):
        session = Session()
        try:
            # Retrieve the card
            card = session.query(Figure_card).filter_by(unique_id=card_id).one_or_none()
            card.state = 'discarded'
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def block_card(card_id: str):
        session = Session()
        try:
            # Retrieve the card
            card = session.query(Figure_card).filter_by(unique_id=card_id).one_or_none()
            card.state = 'blocked'
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

repo = gameRepository()