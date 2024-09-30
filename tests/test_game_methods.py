import unittest
from src.entities.game.game_utils import add_game,get_games, pass_turn, get_game_by_id, add_to_game
from src.entities.player.player_utils import add_player

class test_game_utils(unittest.TestCase):
    def test_add_and_get_game(self):
        darth_id = add_player(player_name="darthVader")
        prevGames = len(get_games())
        for added in range(10):
            assert added+prevGames == len(get_games())
            add_game(game_name = "DeathStar", creator_id = darth_id)
    
    def test_pass_turn(self):
        darth_id = add_player(player_name="darthVader")
        game_id = "0"
        for _ in range(10):
            game_id = add_game(game_name = "DeathStar", creator_id = darth_id)
        assert get_game_by_id(game_id=game_id)['turn'] == 0
        assert get_game_by_id(game_id=game_id)['name'] == "DeathStar"
        assert darth_id in get_game_by_id(game_id=game_id)['players']
        luke_id = add_player(player_name="lukeSky")
        add_to_game(game_id=game_id,player_id=luke_id)
        turn_order = get_game_by_id(game_id=game_id)['players']
        assert len(turn_order) == 2
        NofGames = 10
        for turns in range(NofGames):
            assert get_game_by_id(game_id=game_id)['turn'] == turns
            pass_turn(game_id=game_id, player_id=turn_order[turns%2])
        for _ in range(NofGames):
            pass_turn(game_id=game_id, player_id=darth_id)
        assert get_game_by_id(game_id=game_id)['turn'] <= NofGames+1

if __name__ == "__main__":
    unittest.main()