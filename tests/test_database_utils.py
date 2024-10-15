import unittest
import uuid
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from entities.db.gamesRepo import repo

NofGames = 10
NofPlayers = NofGames*2

#WRITES TO DB
class test_games_Repo(unittest.TestCase):
    def tearDown(self):
        repo.tear_down()
        assert len(repo.get_games()) == 0
    
    def test_create_get_join(self):
        repo.tear_down()
        player_ids = []
        for _ in range(NofPlayers):
            player_ids.append(str(uuid.uuid4()))
            repo.create_player(name="MESSI",unique_id=player_ids[-1])
        game_ids = []
        for _ in range(NofGames):
            game_ids.append(str(uuid.uuid4()))
            repo.create_game(unique_id=game_ids[-1],name = "FUNALDELMUNDIAL",state="waiting",creator_id=player_ids[_])
        games = repo.get_games()
        for game in games:
            assert game['unique_id'] in game_ids
            assert game['creator'] in player_ids
        assert len(games) == len(game_ids)
        assert repo.get_game(game_id=game_ids[0])['creator'] == player_ids[0]
        #try joining
        repo.add_player_to_game(player_id=player_ids[-1],game_id=game_ids[0])
        assert player_ids[-1] in repo.get_game(game_id=game_ids[0])['players']
    
    def test_create_card(self):
        pid,gid = str(uuid.uuid4()),str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="waiting",creator_id=pid)
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state='drawn')
        repo.create_card(card_type=4,card_kind='movement',player_id=pid,game_id=gid)
        player = repo.get_player(pid)
        assert len(player['figure_cards']) == 1
        assert len(player['movement_cards']) == 1
        assert player['movement_cards'][0] == 4
        assert player['figure_cards'][0]['state'] == 'drawn'
        assert player['figure_cards'][0]['type'] == 2
    
    def test_pass_turn(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        game = repo.get_game(game_id=gid)
        assert game['turn'] == 0
        for _ in range(70):
            repo.pass_turn(game_id = gid)
        game = repo.get_game(game_id=gid)
        assert game['turn'] == 70

    def test_take_move_card(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.create_card(card_type=4,card_kind='movement',player_id=None,game_id=gid)
        repo.create_card(card_type=2,card_kind='movement',player_id=None,game_id=gid)
        repo.take_move_card(pid,gid)
        assert len(repo.get_move_deck(gid)) == 1
        assert len(repo.get_player(pid)['movement_cards']) == 1 
    
    def test_drawn_fig_card(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state="not drawn")
        repo.drawn_figure_card(player_id=pid)
        assert repo.get_player(pid)['figure_cards'][0]['state'] == "drawn"
        
    def test_create_board(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)

        repo.create_board(game_id=gid)
        assert len(repo.get_board(game_id=gid)) == 6 
        for x_coordinate in range(6):
            assert len(repo.get_board(game_id=gid)[x_coordinate]) == 6
    
    def test_swap_positions(self):
        pid1 = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid1)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid1)
        repo.add_player_to_game(player_id=pid1,game_id=gid)
        repo.create_board(game_id=gid)
        color1 = repo.get_board(game_id=gid)[0][0]
        color2 = repo.get_board(game_id=gid)[1][0]
        color3 = repo.get_board(game_id=gid)[2][4]
        color4 = repo.get_board(game_id=gid)[2][5]
        repo.swap_positions_board(game_id=gid,x1=0,y1=0,x2=0,y2=1)
        repo.swap_positions_board(game_id=gid,x1=4,y1=2,x2=5,y2=2)
        assert repo.get_board(game_id=gid)[0][0] == color2
        assert repo.get_board(game_id=gid)[1][0] == color1
        assert repo.get_board(game_id=gid)[2][4] == color4
        assert repo.get_board(game_id=gid)[2][5] == color3
        
if __name__ == "__main__":
    unittest.main()