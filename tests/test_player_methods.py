import unittest
from src.entities.game.game_utils import add_game,get_games,delete_all
from src.entities.player.player_utils import add_player,take_move_card,take_figures_card
from src.entities.db.gamesRepo import repo 
import uuid

class test_player_utils(unittest.TestCase):
    def test1_take_move_card(self):

        pid,gid = str(uuid.uuid4()),str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FINALDELMUNDIAL",state="waiting",creator_id=pid)
        
        mov_card_info = take_move_card(pid,gid)
        print("\n --MV-CARD-INFO-- \n")
        print( f"{mov_card_info}\n")
        
        player = repo.get_player(pid)
        self.assertEqual(len(player["movement_cards"]),1)
        
        mov_card_info = take_move_card(pid,gid)
        mov_card_info = take_move_card(pid,gid)
        player = repo.get_player(pid)
        self.assertEqual(len(player["movement_cards"]),3)
        
        print(player["movement_cards"])
        
    def test2_take_figure_cards(self):
        
        pid,gid = str(uuid.uuid4()),str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FINALDELMUNDIAL",state="waiting",creator_id=pid)
        
        
        fg_cards_info = take_figures_card(pid,gid)
        print("\n --FG-CARD-INFO-- \n")
        print( f"{fg_cards_info}\n")
        
        player = repo.get_player(pid)
        self.assertEqual(len(player["figure_cards"]),3)
        
        print(player["figure_cards"])
        
        
    def tearDown(self) -> None:
        repo.tear_down()
        assert len(repo.get_games()) == 0
    

if __name__ == "__main__":
    unittest.main()