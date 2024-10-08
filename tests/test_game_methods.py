import unittest
from src.entities.game.game_utils import add_game,get_games, pass_turn, get_game_by_id, add_to_game, start_game_by_id,get_games_with_player_names,get_players_status, create_figure_cards, create_move_deck_for_game, get_move_deck
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
    
    def test_create_move_deck_for_game(self):
        darth_id = add_player(player_name="darthVader")
        game_id = add_game(game_name = "DeathStar", creator_id = darth_id)
        add_to_game(game_id=game_id,player_id=darth_id)
        create_move_deck_for_game(game_id)
        assert len(get_move_deck(game_id)) == 49
        
    
    def test_create_figure_cards(self):
        darth_id = add_player(player_name="darthVader")
        lukita_id = add_player(player_name="lukita")
        game_id = add_game(game_name = "DeathStar", creator_id = darth_id)
        add_to_game(game_id=game_id,player_id=darth_id)
        add_to_game(game_id=game_id,player_id=lukita_id)
        create_figure_cards(game_id)
        len(get_players_status(game_id)[0]['figure_cards']) == len(get_players_status(game_id)[1]['figure_cards'])      
        
    def test_start_game(self):
        darth_id = add_player(player_name="darthVader")
        lukita_id = add_player(player_name="lukita")
        game_id = add_game(game_name = "DeathStar", creator_id = darth_id)
        add_to_game(game_id=game_id,player_id=lukita_id)
        assert get_game_by_id(game_id=game_id)["state"] == "waiting"
        start_game_by_id(game_id)
        assert get_game_by_id(game_id=game_id)["state"] == "started"
        for player in get_players_status(game_id):
            assert len(player['figure_cards']) == 25
            assert len(player['movement_cards']) == 3

    def test_games_with_names(self):
        games = get_games_with_player_names()
        assert "player_names" in (games[0]).keys()

if __name__ == "__main__":
    unittest.main()