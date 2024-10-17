import unittest
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from entities.game.game_utils import add_game,get_games, pass_turn, add_to_game, start_game_by_id, remove_player_from_game, get_players_names, make_temp_movement

games = [{'unique_id': '1', 'creator': 'ME', 'state': 'waiting', 'players': ['ME', 'p2'], 'player_names': ['MYNAME', 'p2NAME']}, 
         {'unique_id': '2', 'creator': 'also ME', 'state': 'started', 'players': ['also ME', 'p2'], 'turn': 0},
         {'unique_id': '3', 'creator': 'also also ME', 'state': 'waiting', 'players': ['also also ME', 'p2', 'p3', 'p3']}]

# FUNCTIONS THAT WILL BE PATCHED
@pytest.fixture
def mock_repo():
    with patch('entities.game.game_utils.repo') as mock:
        yield mock

@pytest.fixture
def mock_take_move_card():
    with patch('entities.game.game_utils.take_move_card') as mock:
        yield mock

@pytest.fixture
def mock_take_figure_card():
    with patch('entities.game.game_utils.drawn_figure_card') as mock:
        yield mock

def test_add_game_success(mock_repo):
    mock_repo.create_game.return_value = 'lukaModric'
    assert add_game(game_name = "Test_Game", creator_id = 'darthVader') == 'lukaModric'
    mock_repo.add_player_to_game.assert_called_once_with(player_id = 'darthVader', game_id = 'lukaModric')
    mock_repo.create_game.assert_called_once()

def test_get_games(mock_repo):
    mock_repo.get_games.return_value = games
    games_gotten = get_games()
    assert games[0] in games_gotten
    assert games[1] not in games_gotten
    assert games[2] in games_gotten
    mock_repo.get_games.assert_called_once()

def test_add_to_game(mock_repo):
    mock_repo.get_game.return_value = games[0]
    add_to_game(player_id = '9', game_id = '1')
    mock_repo.add_player_to_game.assert_called_once()

def test_add_to_game_started(mock_repo):
    mock_repo.get_game.return_value = games[1]
    assert -1 == add_to_game(player_id = '9', game_id = '1')
    mock_repo.add_player_to_game.assert_not_called()

def test_add_to_game_too_many_players(mock_repo):
    mock_repo.get_game.return_value = games[2]
    assert -1 == add_to_game(player_id = '9', game_id = '1')
    mock_repo.add_player_to_game.assert_not_called()

def test_remove_player_from_game(mock_repo):
    remove_player_from_game('1','1')
    mock_repo.remove_player_from_game.assert_called_once()

def test_get_players_names(mock_repo):
    mock_repo.get_game.return_value = games[0]
    assert get_players_names(game_id = 'A') == games[0]['player_names']
    mock_repo.get_game.assert_called_once

def test_pass_turn_success(mock_repo):
    mock_repo.get_game.return_value = games[1]
    assert pass_turn(game_id = 'Game 2', player_id = 'also ME')
    mock_repo.pass_turn.assert_called_once_with(game_id = 'Game 2')

def test_pass_turn_not_in_game(mock_repo):
    mock_repo.get_game.return_value = games[1]
    assert not pass_turn(game_id = 'Game 2', player_id = 'NOT ME')
    mock_repo.pass_turn.assert_not_called()

def test_pass_turn_not_my_turn(mock_repo):
    mock_repo.get_game.return_value = games[1]
    assert not pass_turn(game_id = 'Game 2', player_id = 'p2')
    mock_repo.pass_turn.assert_not_called()

def test_start_game_by_id(mock_repo, mock_take_move_card, mock_take_figure_card):
    mock_repo.get_game.return_value = games[0]
    start_game_by_id('Game 1')
    mock_repo.edit_game_state.assert_called_once_with('Game 1', 'started')
    mock_take_move_card.assert_called()
    mock_take_figure_card.assert_called()

def test_start_game_by_id_failure(mock_repo, mock_take_move_card, mock_take_figure_card):
    mock_repo.get_game.return_value = games[1]
    try:
        start_game_by_id('Game 2')
    except:
        pass
        #Check that exception was raised
    finally:
        mock_repo.edit_game_state.assert_not_called()
        mock_take_move_card.assert_not_called()
        mock_take_figure_card.assert_not_called()

#TODO MOCK
def test_make_temp_movement_success(mock_repo):
    mock_repo.get_player.return_value = [''{}]

if __name__ == "__main__":
    unittest.main()