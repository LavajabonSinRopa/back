import unittest
import uuid
from src.entities.db.gamesRepo import repo

NofGames = 10
NofPlayers = NofGames*2

class test_games_Repo(unittest.TestCase):
    def test_tear_down(self):
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
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state='Not Drawn')
        repo.create_card(card_type=4,card_kind='movement',player_id=pid,game_id=gid)
        player = repo.get_player(pid)
        assert len(player['figure_cards']) == 1
        assert len(player['movement_cards']) == 1
        assert player['movement_cards'][0] == 4
        assert player['figure_cards'][0]['state'] == 'Not Drawn'
        assert player['figure_cards'][0]['type'] == 2
        

if __name__ == "__main__":
    unittest.main()