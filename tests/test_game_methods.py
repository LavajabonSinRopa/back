import unittest
from src.entities.game.game_utils import add_game,get_games,delete_all
from src.entities.player.player_utils import add_player

class test_game_utils(unittest.TestCase):
    def test_add_and_get_game(self):
        delete_all()
        darth_id = add_player(player_name="darthVader")
        for added in range(100):
            assert added == len(get_games())
            add_game(game_name = "DeathStar", creator_id = darth_id)

    

if __name__ == "__main__":
    unittest.main()