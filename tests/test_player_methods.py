import unittest
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from entities.player.player_utils import add_player, take_move_card, drawn_figure_card

@pytest.fixture
def mock_repo():
    with patch('entities.player.player_utils.repo') as mock:
        yield mock

player_name = 'lali(bertadores)'
card_info = 'blueeyeswhitedragon'


def test_add_player(mock_repo):
    add_player(player_name)
    mock_repo.create_player.assert_called_once

def test_take_move_card(mock_repo):
    take_move_card('X','X')
    mock_repo.take_move_card.assert_called_once()

def test_take_figures_card(mock_repo):
    drawn_figure_card('X')
    mock_repo.drawn_figure_card.assert_called_once()

# class test_player_utils(unittest.TestCase):
#     def test1_take_move_card(self):

#         pid = add_player(player_name="MESSI")
#         gid = add_game(game_name="FINALDELMUNDIAL",creator_id=pid)
        
#         mov_card_info = take_move_card(player_id=pid,game_id=gid)
        
#         print("\n --MV-CARD-INFO-- \n")
#         print( f"{mov_card_info}\n")
        
#         player = repo.get_player(pid)
#         self.assertEqual(len(player["movement_cards"]),1)
        
#         mov_card_info = take_move_card(player_id=pid,game_id=gid)
#         mov_card_info = take_move_card(player_id=pid,game_id=gid)
#         player = repo.get_player(pid)
#         self.assertEqual(len(player["movement_cards"]),3)
        
#         print(player["movement_cards"])
        
#     def test2_take_figure_cards(self):
        
#         pid,gid = str(uuid.uuid4()),str(uuid.uuid4())
#         repo.create_player(name="MESSI",unique_id=pid)
#         repo.create_game(unique_id=gid,name = "FINALDELMUNDIAL",state="waiting",creator_id=pid)
        
        
#         fg_cards_info = take_figures_card(player_id=pid,game_id=gid)
#         print("\n --FG-CARD-INFO-- \n")
#         print( f"{fg_cards_info}\n")
        
#         player = repo.get_player(pid)
#         self.assertEqual(len(player["figure_cards"]),3)
        
#         print(player["figure_cards"])
        
        
#     def tearDown(self) -> None:
#         repo.tear_down()
#         assert len(repo.get_games()) == 0
    

if __name__ == "__main__":
    unittest.main()