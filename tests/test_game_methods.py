import unittest
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from entities.game.game_utils import add_game,get_games, pass_turn, add_to_game, start_game_by_id, remove_player_from_game, get_players_names, get_player_name , make_temp_movement, highlight_figures, remove_top_movement, apply_temp_movements, complete_figure, block_figure

games = [{'unique_id': '1', 'creator': 'ME', 'state': 'waiting', 'players': ['ME', 'p2'], 'player_names': ['MYNAME', 'p2NAME']}, 
         {'unique_id': '2', 'creator': 'also ME', 'state': 'started', 'players': ['also ME', 'p2'], 'turn': 0},
         {'unique_id': '3', 'creator': 'also also ME', 'state': 'waiting', 'players': ['also also ME', 'p2', 'p3', 'p3']},
         {'unique_id': 'adb7026d-cf96-4bac-937b-a8106e56f160', 'name': 'GAME3', 'state': 'started', 
          'board': [['figure', 'figure', 'figure', 'blue', 'red', 'blue'], 
                    ['figure', 'green', 'green', 'yellow', 'blue', 'red'], 
                    ['blue', 'blue', 'yellow', 'yellow', 'yellow', 'green'], 
                    ['green', 'red', 'yellow', 'green', 'green', 'red'], 
                    ['yellow', 'blue', 'red', 'yellow', 'green', 'figure'], 
                    ['red', 'green', 'red', 'figure', 'figure', 'figure']],
          'turn': 1, 'creator': 'fbe2bf36-dc11-470e-a61e-4774b4d4aa23', 
          'players': [{'unique_id': '67ab34c4-052f-4683-be84-5886f26b864e', 'name': 'EL', 
                       'figure_cards': [{'type': 6, 'state': 'drawn', 'unique_id': '1'}, {'type': 6, 'state': 'drawn', 'unique_id': '405'}, {'type': 21, 'state': 'drawn', 'unique_id' : '2'}], 
                       'movement_cards': [{'type': 0, 'unique_id': '9277905e-b02b-4605-a0af-4ab509c9967e', 'state': None}, {'type': 0, 'unique_id': '3d7b9a1f-bbcd-4e56-938d-e4fe15e51ddb', 'state': None}, {'type': 0, 'unique_id': 'fc2c43d9-fd5e-4654-89b4-1911157eda28', 'state': None}]}, 
                      {'unique_id': 'fbe2bf36-dc11-470e-a61e-4774b4d4aa23', 'name': 'YO', 
                       'figure_cards': [{'type': 6, 'state': 'drawn', 'unique_id': '1'}, {'type': 6, 'state': 'drawn', 'unique_id': '405'}, {'type': 21, 'state': 'drawn', 'unique_id' : '2'}], 
                       'movement_cards': [{'type': 0, 'unique_id': '7bf11638-26cd-45ce-8812-98810ba30776', 'state': None}, {'type': 0, 'unique_id': 'b4b20c32-1156-4ab1-9f80-bd57093e89e4', 'state': None}, {'type': 0, 'unique_id': 'd4e79bc8-e840-4ea3-9558-1baa681b4599', 'state': None}],
                       'movements': [{'from_x': 0, 'from_y': 0, 'to_x': 5, 'to_y': 5}]}]},
        {'unique_id': 'adb7026d-cf96-4bac-937b-a8106e56f160', 'name': 'GAME3', 'state': 'started', 
          'board': [['figure', 'figure', 'figure', 'blue', 'red', 'blue'], 
                    ['figure', 'figure', 'green', 'yellow', 'blue', 'red'], 
                    ['blue', 'blue', 'yellow', 'yellow', 'yellow', 'green'], 
                    ['green', 'red', 'yellow', 'green', 'green', 'red'], 
                    ['yellow', 'blue', 'red', 'yellow', 'green', 'figure'], 
                    ['red', 'green', 'red', 'figure', 'figure', 'figure']],
          'turn': 1, 'creator': 'fbe2bf36-dc11-470e-a61e-4774b4d4aa23', 
          'players': ['67ab34c4-052f-4683-be84-5886f26b864e']}
]

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

def test_get_player_name_success(mock_repo):
    mock_repo.get_player.return_value = {"name": "Messi", "unique_id": "123"}
    result = get_player_name("123")
    assert result == "Messi"
    mock_repo.get_player.assert_called_once_with("123")


def test_pass_turn_success(mock_repo, mock_take_move_card):
    mock_repo.get_game.return_value = games[1]
    assert pass_turn(game_id = 'Game 2', player_id = 'also ME')
    mock_repo.pass_turn.assert_called_once_with(game_id = 'Game 2')
    mock_take_move_card.assert_called()

def test_pass_turn_not_in_game(mock_repo,mock_take_move_card):
    mock_repo.get_game.return_value = games[1]
    assert not pass_turn(game_id = 'Game 2', player_id = 'NOT ME')
    mock_repo.pass_turn.assert_not_called()
    mock_take_move_card.assert_not_called()

def test_pass_turn_not_my_turn(mock_repo,mock_take_move_card):
    mock_repo.get_game.return_value = games[1]
    assert not pass_turn(game_id = 'Game 2', player_id = 'p2')
    mock_repo.pass_turn.assert_not_called()
    mock_take_move_card.assert_not_called()

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

def test_make_temp_movement_success(mock_repo):
    mock_repo.get_player.return_value = games[3]['players'][1]
    mock_repo.add_movement.return_value = 0
    player = games[3]['players'][1]
    card = player['movement_cards'][0]
    assert make_temp_movement(game_id = games[3]['unique_id'], player_id = player['unique_id'], card_id = card['unique_id'], from_x = 0, from_y = 0, to_x = 2, to_y = 2)
    mock_repo.get_player.assert_called_once_with(player_id = player['unique_id'])
    mock_repo.add_movement.assert_called_once_with(player_id = player['unique_id'], from_x=0, from_y=0, to_x=2, to_y=2, card_id=card['unique_id'])
    mock_repo.swap_positions_board.assert_called_once_with(game_id=games[3]['unique_id'], x1=0, y1=0, x2=2, y2=2)

def test_make_temp_movement_failure_on_getting_player(mock_repo):
    mock_repo.get_player.side_effect = Exception("TEST")
    player = games[3]['players'][1]
    card = player['movement_cards'][0]
    try: 
        make_temp_movement(game_id = games[3]['unique_id'],player_id = player['unique_id'], card_id = card['unique_id'], from_x = 0, from_y = 0, to_x = 2, to_y = 2)
        assert False
    except:
        pass
    finally:
        mock_repo.get_player.assert_called_once_with(player_id = player['unique_id'])
        mock_repo.add_movement.assert_not_called()
        mock_repo.swap_positions_board.assert_not_called()

def test_make_temp_movement_failure_on_movement(mock_repo):
    mock_repo.add_movement.side_effect = Exception("TEST")
    player = games[3]['players'][1]
    card = player['movement_cards'][0]
    try: 
        make_temp_movement(game_id = games[3]['unique_id'],player_id = player['unique_id'], card_id = card['unique_id'], from_x = 0, from_y = 0, to_x = 2, to_y = 2)
        assert False
    except:
        pass
    finally:
        mock_repo.get_player.assert_called_once_with(player_id = player['unique_id'])
        mock_repo.add_movement.assert_not_called()
        mock_repo.swap_positions_board.assert_not_called()

def test_make_temp_movement_cant_move(mock_repo):
    mock_repo.get_player.return_value = games[3]['players'][1]
    mock_repo.add_movement.return_value = 0
    player = games[3]['players'][1]
    card = player['movement_cards'][0]
    assert not make_temp_movement(game_id = games[3]['unique_id'], player_id = player['unique_id'], card_id = card['unique_id'], from_x = 0, from_y = 0, to_x = 4, to_y = 2)
    mock_repo.get_player.assert_called_once_with(player_id = player['unique_id'])
    mock_repo.add_movement.assert_not_called()
    mock_repo.swap_positions_board.assert_not_called()

def test_make_temp_movement_outside_board(mock_repo):
    mock_repo.get_player.return_value = games[3]['players'][1]
    mock_repo.add_movement.return_value = 0
    player = games[3]['players'][1]
    card = player['movement_cards'][0]
    try:
        assert not make_temp_movement(game_id = games[3]['unique_id'], player_id = player['unique_id'], card_id = card['unique_id'], from_x = 0, from_y = 0, to_x = -4, to_y = 2)
        assert False
    except:
        pass    
    finally:
        mock_repo.get_player.assert_not_called()
        mock_repo.add_movement.assert_not_called()
        mock_repo.swap_positions_board.assert_not_called()

def test_highlight_figures():
    board = [['g','g','g','g','g','x'],['b','b','b','b','x','x'],['a','a','a','a','x','x'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p']]
    expected_result = [['G','G','G','G','G','X'],['B','B','B','B','X','X'],['A','A','A','A','X','X'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p']]
    assert expected_result == highlight_figures(board)

    board = [['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['g','g','g','g','g','x'],['b','b','b','b','x','x'],['a','a','a','a','x','x'],]
    expected_result = [['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['G','G','G','G','G','X'],['B','B','B','B','X','X'],['A','A','A','A','X','X']]
    assert expected_result == highlight_figures(board)

    board = [['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p'],['p','p','p','p','p','p']]
    assert board == highlight_figures(board)

def test_complete_figure_success(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]

    assert complete_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][0]['figure_cards'][0]['unique_id'], i = 5, j = 5)

    mock_repo.apply_temp_movements.assert_called_once()
    mock_repo.discard_card.assert_called_once_with(card_id='1')

    assert complete_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][0]['figure_cards'][2]['unique_id'], i = 0, j = 1)
    
    mock_repo.discard_card.assert_called_with(card_id='2')


def test_complete_figure_not_in_game(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        complete_figure(game_id = games[3]['unique_id'], player_id = "No estoy en la partida", card_id = games[3]['players'][0]['figure_cards'][0]['unique_id'], i = 5, j = 5)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.discard_card.assert_not_called()

def test_complete_figure_no_card(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        complete_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = "No soy una carta", i = 5, j = 5)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.discard_card.assert_not_called()

def test_complete_figure_out_of_bounds(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        complete_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][0]['figure_cards'][0]['unique_id'], i = 31, j = -5)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.discard_card.assert_not_called()

def test_complete_figure_failure(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        complete_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][0]['figure_cards'][0]['unique_id'], i = 2, j = 1)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.discard_card.assert_not_called()
    try:
        complete_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][0]['figure_cards'][0]['unique_id'], i = 0, j = 1)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.discard_card.assert_not_called()

def test_block_figure_success(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_game_status.return_value = games[3]
    mock_repo.get_player.return_value = games[3]['players'][0]

    assert block_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][1]['figure_cards'][0]['unique_id'], i = 5, j = 5)

    mock_repo.apply_temp_movements.assert_called_once()
    mock_repo.block_card.assert_called_once_with(card_id='1')

    assert block_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][1]['figure_cards'][2]['unique_id'], i = 0, j = 1)
    
    mock_repo.block_card.assert_called_with(card_id='2')


def test_block_figure_not_in_game(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        block_figure(game_id = games[3]['unique_id'], player_id = "No estoy en la partida", card_id = games[3]['players'][1]['figure_cards'][0]['unique_id'], i = 5, j = 5)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.block_card.assert_not_called()

def test_block_figure_no_card(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        block_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = "No soy una carta", i = 5, j = 5)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.block_card.assert_not_called()

def test_block_figure_out_of_bounds(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        block_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][1]['figure_cards'][0]['unique_id'], i = 31, j = -5)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.block_card.assert_not_called()

def test_block_figure_failure(mock_repo):
    mock_repo.get_game.return_value = games[4]
    mock_repo.get_player.return_value = games[3]['players'][0]
    try:
        block_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][1]['figure_cards'][0]['unique_id'], i = 2, j = 1)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.block_card.assert_not_called()
    try:
        block_figure(game_id = games[3]['unique_id'], player_id = games[3]['players'][0]['unique_id'], card_id = games[3]['players'][1]['figure_cards'][0]['unique_id'], i = 0, j = 1)
        assert False
    except:
        mock_repo.apply_temp_movements.assert_not_called()
        mock_repo.block_card.assert_not_called()

if __name__ == "__main__":
    unittest.main()