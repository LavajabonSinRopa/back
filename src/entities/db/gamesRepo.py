from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from .models import Game, Player, engine
from typing import List

# Create a session
Session = sessionmaker(bind=engine)

class gameRepository:
    @staticmethod
    def create_game(unique_id: str,name: str, state: str, creator_id: str) -> Game:
        session = Session()
        try:
            new_game = Game(unique_id = unique_id, name=name, state=state, creator=creator_id)
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
            print(name)
            print(unique_id)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
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
                "creator": game.creator,
                "players": [player.unique_id for player in game.players]
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

repo = gameRepository()