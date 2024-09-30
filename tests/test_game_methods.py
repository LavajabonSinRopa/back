import unittest
from src.entities.game.game_utils import add_game,get_games,delete_all,start_game_by_id
from src.entities.player.player_utils import add_player

class test_game_utils(unittest.TestCase):
    def test_add_and_get_game(self):
        delete_all()
        darth_id = add_player(player_name="darthVader")
        for added in range(100):
            assert added == len(get_games())
            add_game(game_name = "DeathStar", creator_id = darth_id)
    
    def test_start_game(self):
        delete_all()
        darth_id = add_player(player_name="darthVader")
        game_id = add_game(game_name = "DeathStar", creator_id = darth_id)
        assert get_games()[0]["state"] == "waiting"
        start_game_by_id(game_id)
        assert get_games()[0]["state"] == "started"
        
    
    

if __name__ == "__main__":
    unittest.main()