import unittest
from src.entities.game.game import Game
from src.entities.game.game_utils import add_game,get_games
from src.entities.player.player import Player


class test_game_utils(unittest.TestCase):
    def test_add_and_get_game(self):
        darth_vader = Player(name = "luke")
        added = []
        for _ in range(100):
            assert len(added) == len(get_games())
            new_game = Game(name = "DeathStar", creator = darth_vader)
            added.append(new_game.unique_id)
            add_game(new_game)
        all_games = get_games()
        for game in added:
            assert game in all_games
    

if __name__ == "__main__":
    unittest.main()