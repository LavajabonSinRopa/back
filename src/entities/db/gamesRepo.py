from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from .models import Game, Player, engine, Figure_card, Movement_card, Table
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
                "board": game.board,
                "turn": game.turn,
                "creator": game.creator,
                "players": [player.unique_id for player in game.players]
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
            print('PLAYER FOUND')
            print(player)
            return {
                "unique_id": player.unique_id,
                "name": player.name,
                "figure_cards": [{'type':fcard.card_type,'state':fcard.state} for fcard in player.figure_cards],
                "movement_cards": [mcard.card_type for mcard in player.movement_cards]
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
                    "board": game.board,
                    "turn": game.turn,
                    "creator": game.creator,
                    "players": [player.unique_id for player in game.players]
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
            session.query(Table).delete()
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
    def create_table(game_id: str):
        session = Session()
        game = session.query(Game).filter_by(unique_id=game_id).one_or_none()
        
        colors = ['red', 'green', 'blue', 'yellow']
        
        try:
            if game is None:
                raise ValueError(f"No game found with ID: {game_id}")
            
            for x in range(6):
                for y in range(6):
                    color = random.choice(colors)
                    table = Table(unique_id=str(uuid.uuid4()), x_coordinate=x, y_coordinate=y, color=color, game_id=game_id)
                    session.add(table)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating table: {e}")
        finally:
            session.close()
            
    @staticmethod
    def get_table(game_id:str) -> List[List[str]]:
        session = Session()
        try:
            tables = session.query(Table).filter_by(game_id=game_id).all()
            
            table_matrix = [[None for _ in range(6)] for _ in range(6)]
            
            for table in tables:
                table_matrix[table.x_coordinate][table.y_coordinate] = table.color
            return table_matrix
        except Exception as e:
            print(f"Error getting table: {e}")
        finally:
            session.close()
repo = gameRepository()