import unittest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main
from entities.game import game_utils
from entities.game.game_utils import FigureResult
from entities.player import player_utils
from interfaces import SocketManagers

# Create a TestClient for the FastAPI app
client = TestClient(main.app)

# FUNCTIONS THAT WILL BE PATCHED
@pytest.fixture
def mock_add_player():
    with patch('interfaces.game_endpoints.add_player') as mock:
        yield mock

@pytest.fixture
def mock_add_game():
    with patch('interfaces.game_endpoints.add_game') as mock:
        yield mock

@pytest.fixture
def mock_get_games():
    with patch('interfaces.game_endpoints.get_games') as mock:
        yield mock

@pytest.fixture
def mock_game_socket_manager():
    with patch('interfaces.game_endpoints.game_socket_manager') as mock:
        yield mock

@pytest.fixture
def mock_public_manager():
    with patch('interfaces.game_endpoints.game_socket_manager') as mock:
        yield mock

@pytest.fixture
def mock_get_game_by_id():
    with patch('interfaces.game_endpoints.get_game_by_id') as mock:
        yield mock

@pytest.fixture
def mock_add_to_game():
    with patch('interfaces.game_endpoints.add_to_game') as mock:
        yield mock

@pytest.fixture
def mock_remove_player_from_game():
    with patch('interfaces.game_endpoints.remove_player_from_game') as mock:
        yield mock

@pytest.fixture
def mock_pass_turn():
    with patch('interfaces.game_endpoints.pass_turn') as mock:
        yield mock

@pytest.fixture
def mock_is_players_turn():
    with patch('interfaces.game_endpoints.is_players_turn') as mock:
        yield mock

@pytest.fixture
def mock_make_temp_movement():
    with patch('interfaces.game_endpoints.make_temp_movement') as mock:
        yield mock

@pytest.fixture
def mock_get_game_status():
    with patch('interfaces.game_endpoints.get_game_status') as mock:
        yield mock

@pytest.fixture
def mock_remove_top_movement():
    with patch('interfaces.game_endpoints.remove_top_movement') as mock:
        yield mock

@pytest.fixture
def mock_apply_temp_movements():
    with patch('interfaces.game_endpoints.apply_temp_movements') as mock:
        yield mock

@pytest.fixture
def mock_complete_figure():
    with patch('interfaces.game_endpoints.complete_figure') as mock:
        yield mock

@pytest.fixture
def mock_block_figure():
    with patch('interfaces.game_endpoints.block_figure') as mock:
        yield mock

@pytest.fixture
def mock_finish_game():
    with patch('interfaces.game_endpoints.finish_game') as mock:
        yield mock
        
@pytest.fixture
def mock_get_player_name():
    with patch('interfaces.game_endpoints.get_player_name') as mock:
        yield mock


def test_create_game_success(mock_add_player, mock_add_game, mock_game_socket_manager, mock_get_games):
    # Arrange
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_add_game.return_value = '42'  # Mock the game ID
    mock_get_games.return_value = []  # Return an empty list for created games
    
    # Create a valid request
    request_data = {
        "game_name": "Test Game",
        "player_name": "Test Player"
    }

    # Act
    response = client.post("/games", json=request_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"game_id": '42', "player_id": '1'}
    mock_add_player.assert_called_once_with(player_name="Test Player")
    mock_add_game.assert_called_once_with(game_name="Test Game", creator_id='1', password = "")
    mock_game_socket_manager.create_game_map.assert_called_once_with('42')
    mock_game_socket_manager.join_player_to_game_map.assert_called_once_with('42', '1')

def test_create_game_success_private(mock_add_player, mock_add_game, mock_game_socket_manager, mock_get_games):
    # Arrange
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_add_game.return_value = '42'  # Mock the game ID
    mock_get_games.return_value = []  # Return an empty list for created games
    
    # Create a valid request
    request_data = {
        "game_name": "Test Game",
        "player_name": "Test Player",
        "password": "1234"
    }

    # Act
    response = client.post("/games", json=request_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"game_id": '42', "player_id": '1'}
    mock_add_player.assert_called_once_with(player_name="Test Player")
    mock_add_game.assert_called_once_with(game_name="Test Game", creator_id='1', password = "1234")
    mock_game_socket_manager.create_game_map.assert_called_once_with('42')
    mock_game_socket_manager.join_player_to_game_map.assert_called_once_with('42', '1')



def test_create_game_empty_name(mock_add_player, mock_add_game, mock_game_socket_manager, mock_get_games):
    
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_add_game.return_value = '42'  # Mock the game ID
    mock_get_games.return_value = []  # Return an empty list for created games
    # Arrange
    request_data = {
        "game_name": "",
        "player_name": "Test Player"
    }

    # Act
    response = client.post("/games", json=request_data)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "El nombre no puede estar vacío"}
    mock_add_player.assert_not_called()
    mock_add_game.assert_not_called()
    mock_game_socket_manager.assert_not_called()

def test_join_game_success(mock_add_player, mock_game_socket_manager, mock_get_games, mock_get_game_by_id, mock_add_to_game):
    
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_get_games.return_value = []  # Return an empty list for created games
    mock_get_game_by_id.return_value = {'players': ['0'], 'state': 'waiting'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_name': 'Test_Player'}
    response = client.post("/games/Test_Game/join", json=request_data)

    assert response.status_code == 200
    assert response.json()['player_id'] == '1'
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_add_player.assert_called_once_with(player_name='Test_Player')
    mock_add_to_game.assert_called_once_with(player_id='1', game_id='Test_Game', password='')
    mock_game_socket_manager.broadcast_game.assert_called_once_with('Test_Game', {'type': 'PlayerJoined', 'payload': {'player_id': '1', 'player_name': 'Test_Player'}})

def test_join_game_failure(mock_add_player, mock_game_socket_manager, mock_get_games, mock_get_game_by_id, mock_add_to_game):
    
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_get_games.return_value = []  # Return an empty list for created games
    mock_get_game_by_id.side_effect = Exception("TEST")
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_name': 'Test_Player'}
    response = client.post("/games/Test_Game/join", json=request_data)

    assert response.status_code == 404
    mock_add_player.assert_not_called
    mock_add_to_game.assert_not_called
    mock_game_socket_manager.broadcast_game.assert_not_called


def test_join_game_full(mock_add_player, mock_game_socket_manager, mock_get_games, mock_get_game_by_id, mock_add_to_game):
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_get_games.return_value = []  # Return an empty list for created games
    mock_get_game_by_id.return_value = {'players': ['0','2','49','YO'], 'state': 'waiting'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_name': 'Test_Player'}
    response = client.post("/games/Test_Game/join", json=request_data)

    assert response.status_code == 403
    mock_add_player.assert_not_called
    mock_add_to_game.assert_not_called

def test_join_not_waiting(mock_add_player, mock_game_socket_manager, mock_get_games, mock_get_game_by_id, mock_add_to_game):
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_get_games.return_value = []  # Return an empty list for created games
    mock_get_game_by_id.return_value = {'players': ['49','YO'], 'state': 'started'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_name': 'Test_Player'}
    response = client.post("/games/Test_Game/join", json=request_data)

    assert response.status_code == 403
    mock_add_player.assert_not_called
    mock_add_to_game.assert_not_called
    mock_game_socket_manager.broadcast_game.assert_not_called

def test_join_game_success_private(mock_add_player, mock_game_socket_manager, mock_get_games, mock_get_game_by_id, mock_add_to_game):
    
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_get_games.return_value = []  # Return an empty list for created games
    mock_get_game_by_id.return_value = {'players': ['0'], 'state': 'waiting'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_name': 'Test_Player', 'password': '1234'}
    response = client.post("/games/Test_Game/join", json=request_data)

    assert response.status_code == 200
    assert response.json()['player_id'] == '1'
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_add_player.assert_called_once_with(player_name='Test_Player')
    mock_add_to_game.assert_called_once_with(player_id='1', game_id='Test_Game', password='1234')
    mock_game_socket_manager.broadcast_game.assert_called_once_with('Test_Game', {'type': 'PlayerJoined', 'payload': {'player_id': '1', 'player_name': 'Test_Player'}})

def test_join_game_fail_private_bad_pasword(mock_add_player, mock_game_socket_manager, mock_get_games, mock_get_game_by_id, mock_add_to_game):
    
    mock_add_player.return_value = '1'  # Mock the player ID
    mock_get_games.return_value = []  # Return an empty list for created games
    mock_get_game_by_id.return_value = {'players': ['0'], 'state': 'waiting'}
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_add_to_game.side_effect = ValueError("Incorrect password")

    request_data = {'player_name': 'Test_Player', 'password': 'Bad password'}
    response = client.post("/games/Test_Game/join", json=request_data)

    assert response.status_code == 403
    mock_add_player.assert_not_called
    mock_add_to_game.assert_not_called
    mock_game_socket_manager.broadcast_game.assert_not_called





def test_leave_game_success(mock_get_game_status, mock_get_game_by_id, mock_remove_player_from_game, mock_game_socket_manager, mock_finish_game, mock_get_player_name):
    
    mock_get_game_by_id.return_value = {'players': ['0','Test_Player'], 'state': 'waiting', 'creator': '0', 'player_names': ['mauri', 'rimau']}
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_player_name.return_value = "Test_Player"
    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/leave", json=request_data)

    assert response.status_code == 200
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_remove_player_from_game.assert_called_once_with(game_id = "Test_Game", player_id = "Test_Player")
    mock_game_socket_manager.broadcast_game.assert_called_with('Test_Game', {'type': 'GameWon', 'payload': {'player_id': '0', 'player_name': 'mauri'}})

def test_leave_game_creator(mock_get_game_status, mock_get_game_by_id, mock_remove_player_from_game, mock_game_socket_manager):
    
    mock_get_game_by_id.return_value = {'players': ['0','Test_Player'], 'state': 'waiting', 'creator': '0'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_id': '0'}
    response = client.post("/games/Test_Game/leave", json=request_data)

    assert response.status_code == 403
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_remove_player_from_game.assert_not_called

def test_leave_game_no_game(mock_get_game_status, mock_get_game_by_id, mock_remove_player_from_game, mock_game_socket_manager):
    
    mock_get_game_by_id.side_effect = Exception("TEST")
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_game_socket_manager.broadcast_game.return_value = "MESI"

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/leave", json=request_data)

    assert response.status_code == 404
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_remove_player_from_game.assert_not_called()
    mock_game_socket_manager.broadcast_game.assert_not_called()


def test_leave_game_not_in_game(mock_get_game_status, mock_get_game_by_id, mock_remove_player_from_game, mock_game_socket_manager):
    
    mock_get_game_by_id.return_value = {'players': ['0','Test_Player'], 'state': 'waiting', 'creator': '0'}
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_remove_player_from_game.side_effect = Exception("TEST")

    request_data = {'player_id': 'Not_THE_Test_Player'}
    response = client.post("/games/Test_Game/leave", json=request_data)

    assert response.status_code != 200
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_remove_player_from_game.assert_not_called

def test_skip_turn_success(mock_get_game_status, mock_pass_turn, mock_game_socket_manager, mock_get_player_name):
    mock_pass_turn.return_value = True
    mock_get_game_status.return_value = []
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_player_name.return_value = "Test_Player"

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/skip", json=request_data)

    assert response.status_code == 200
    mock_pass_turn.assert_called_once_with(game_id = "Test_Game", player_id = "Test_Player")

def test_skip_turn_not_their_turn(mock_pass_turn):
    mock_pass_turn.return_value = False

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/skip", json=request_data)

    assert response.status_code != 200
    mock_pass_turn.assert_called_once_with(game_id = "Test_Game", player_id = "Test_Player")

def test_skip_turn_not_in_game(mock_pass_turn):
    mock_pass_turn.side_effect = Exception("TEST")

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/skip", json=request_data)

    assert response.status_code != 200
    mock_pass_turn.assert_called_once_with(game_id = "Test_Game", player_id = "Test_Player")

def test_get_all_games(mock_get_games):
    mock_get_games.return_value = []  # Return an empty list for created games

    response = client.get("/games")
    assert response.status_code == 200

def test_make_temp_move_success(mock_get_game_status, mock_game_socket_manager,mock_is_players_turn, mock_make_temp_movement, mock_get_player_name):
    mock_is_players_turn.return_value = True
    mock_make_temp_movement.return_value = True
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_get_player_name.return_value = "Test_Player"

    request_data = {'player_id': 'Test_Player','card_id': '100', 'from_x': 1, 'from_y': 1, 'to_x': 1, 'to_y': 1}
    response = client.post("/games/Test_Game/move", json=request_data)

    assert response.status_code == 200
    mock_is_players_turn.assert_called_once_with(player_id='Test_Player', game_id='Test_Game')
    mock_make_temp_movement.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='100', from_x=1, from_y=1, to_x=1, to_y=1)
    mock_game_socket_manager.broadcast_game.assert_called()
    mock_get_game_status.assert_called_once()

def test_make_temp_move_cant_find_game(mock_get_game_status, mock_game_socket_manager,mock_is_players_turn, mock_make_temp_movement):
    mock_is_players_turn.side_effect = Exception("TEST")
    mock_make_temp_movement.return_value = True
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []

    request_data = {'player_id': 'Test_Player','card_id': '100', 'from_x': 1, 'from_y': 1, 'to_x': 1, 'to_y': 1}
    response = client.post("/games/Test_Game/move", json=request_data)

    assert response.status_code == 404
    mock_is_players_turn.assert_called_once_with(player_id='Test_Player', game_id='Test_Game')
    mock_make_temp_movement.assert_not_called()
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_get_game_status.assert_not_called()

def test_make_temp_move_not_their_turn(mock_get_game_status, mock_game_socket_manager,mock_is_players_turn, mock_make_temp_movement):
    mock_is_players_turn.return_value = False
    mock_make_temp_movement.return_value = True
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []

    request_data = {'player_id': 'Test_Player','card_id': '100', 'from_x': 1, 'from_y': 1, 'to_x': 1, 'to_y': 1}
    response = client.post("/games/Test_Game/move", json=request_data)

    assert response.status_code == 404
    mock_is_players_turn.assert_called_once_with(player_id='Test_Player', game_id='Test_Game')
    mock_make_temp_movement.assert_not_called()
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_get_game_status.assert_not_called()


def test_make_temp_move_failure_to_make_move(mock_get_game_status, mock_game_socket_manager,mock_is_players_turn, mock_make_temp_movement):
    mock_is_players_turn.return_value = True
    mock_make_temp_movement.side_effect = Exception("TEST")
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []

    request_data = {'player_id': 'Test_Player','card_id': '100', 'from_x': 1, 'from_y': 1, 'to_x': 1, 'to_y': 1}
    response = client.post("/games/Test_Game/move", json=request_data)

    assert response.status_code == 500
    mock_is_players_turn.assert_called_once_with(player_id='Test_Player', game_id='Test_Game')
    mock_make_temp_movement.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='100', from_x=1, from_y=1, to_x=1, to_y=1)
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_get_game_status.assert_not_called()

def test_make_unmove_success(mock_get_game_status, mock_game_socket_manager,mock_is_players_turn, mock_remove_top_movement, mock_get_player_name):
    mock_is_players_turn.return_value = True
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_get_player_name.return_value = "Test_Player"

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/unmove", json=request_data)

    assert response.status_code == 200
    mock_is_players_turn.assert_called_once_with(player_id='Test_Player', game_id='Test_Game')
    mock_remove_top_movement.assert_called_once_with(game_id='Test_Game', player_id='Test_Player')
    mock_game_socket_manager.broadcast_game.assert_called()
    mock_get_game_status.assert_called_once()

def test_make_unmove_failure_no_turn(mock_get_game_status, mock_game_socket_manager,mock_is_players_turn, mock_remove_top_movement):
    mock_is_players_turn.return_value = False
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/unmove", json=request_data)

    assert response.status_code == 404
    mock_is_players_turn.assert_called_once_with(player_id='Test_Player', game_id='Test_Game')
    mock_remove_top_movement.assert_not_called()
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_get_game_status.assert_not_called()
    
def test_apply_move_success(mock_get_game_status, mock_game_socket_manager, mock_is_players_turn,mock_apply_temp_movements, mock_get_player_name):
    mock_is_players_turn.return_value = True
    mock_apply_temp_movements.return_value = True
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_get_player_name.return_value = "Test_Player"

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/apply", json=request_data)

    assert response.status_code == 200
    mock_apply_temp_movements.assert_called_once_with(game_id='Test_Game', player_id='Test_Player')
    mock_game_socket_manager.broadcast_game.assert_called()
    mock_get_game_status.assert_called_once()

def test_apply_move_failure_no_turn(mock_get_game_status, mock_game_socket_manager, mock_is_players_turn, mock_apply_temp_movements):
    mock_is_players_turn.return_value = False
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/apply", json=request_data)

    assert response.status_code == 403
    mock_apply_temp_movements.assert_not_called()
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_get_game_status.assert_not_called()


def test_complete_figure_player_wins(mock_get_game_status, mock_game_socket_manager, mock_complete_figure, mock_get_game_by_id, mock_finish_game, mock_get_player_name):
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_complete_figure.return_value = FigureResult.PLAYER_WON  
    mock_get_game_by_id.return_value = {"players": ["Test_Player", "Player2"],"player_names": ["Winner", "Loser"]}

    request_data = {'player_id': 'Test_Player', 'x' : 1, 'y' : 4, 'card_id' : 'test_card'}
    response = client.post("/games/Test_Game/completeFigure", json=request_data)
    print(response)
    assert response.status_code == 200
    mock_complete_figure.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='test_card', i=4, j=1)
    mock_get_game_by_id.assert_called_once_with('Test_Game')
    mock_game_socket_manager.broadcast_game.assert_called_once_with('Test_Game',{"type":"GameWon","payload": {'player_id' : 'Test_Player', 'player_name': 'Winner'}})

def test_complete_figure_success(mock_get_game_status, mock_game_socket_manager, mock_complete_figure, mock_get_player_name):
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_complete_figure.return_value = FigureResult.COMPLETED
    mock_get_player_name.return_value = "Test_Player"

    request_data = {'player_id': 'Test_Player', 'x' : 1, 'y' : 4, 'card_id' : 'test_card'}
    response = client.post("/games/Test_Game/completeFigure", json=request_data)

    assert response.status_code == 200
    mock_complete_figure.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='test_card', i=4, j=1)
    mock_game_socket_manager.broadcast_game.assert_called()

def test_complete_figure_failure(mock_get_game_status, mock_game_socket_manager, mock_complete_figure):
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_complete_figure.side_effect = Exception("test")

    request_data = {'player_id': 'Test_Player', 'x' : 1, 'y' : 4, 'card_id' : 'test_card'}
    response = client.post("/games/Test_Game/completeFigure", json=request_data)

    assert response.status_code == 403
    mock_complete_figure.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='test_card', i=4, j=1)
    mock_game_socket_manager.broadcast_game.assert_not_called()

def test_block_figure_success(mock_get_game_status, mock_game_socket_manager, mock_block_figure, mock_get_player_name):
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_get_player_name.return_value = "Test_Player"
    mock_block_figure.return_value = (FigureResult.COMPLETED, "blocked_player_id")
    request_data = {'player_id': 'Test_Player', 'x' : 1, 'y' : 4, 'card_id' : 'test_card'}
    response = client.post("/games/Test_Game/blockFigure", json=request_data)

    assert response.status_code == 200
    mock_block_figure.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='test_card', i=4, j=1)
    mock_game_socket_manager.broadcast_game.assert_called()

def test_block_figure_failure(mock_get_game_status, mock_game_socket_manager, mock_block_figure):
    mock_game_socket_manager.broadcast_game = AsyncMock()
    mock_get_game_status.return_value = []
    mock_block_figure.side_effect = Exception("test")

    request_data = {'player_id': 'Test_Player', 'x' : 1, 'y' : 4, 'card_id' : 'test_card'}
    response = client.post("/games/Test_Game/blockFigure", json=request_data)

    assert response.status_code == 403
    mock_block_figure.assert_called_once_with(game_id='Test_Game', player_id='Test_Player', card_id='test_card', i=4, j=1)
    mock_game_socket_manager.broadcast_game.assert_not_called()

def test_cancel_game_success(mock_get_game_by_id, mock_game_socket_manager, mock_finish_game):
    mock_get_game_by_id.return_value = {'players': ['0', 'Test_Player'], 'state': 'waiting', 'creator': 'Test_Player'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/cancel", json=request_data)

    assert response.status_code == 200
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_game_socket_manager.broadcast_game.assert_called_once_with('Test_Game', {"type": "GameClosed", "payload": "Game Closed, disconnected"})
    mock_finish_game.assert_called_once_with("Test_Game")

def test_cancel_game_not_creator(mock_get_game_by_id, mock_game_socket_manager, mock_finish_game):
    mock_get_game_by_id.return_value = {'players': ['0', 'Test_Player'], 'state': 'waiting', 'creator': '0'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/cancel", json=request_data)

    assert response.status_code == 403
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_finish_game.assert_not_called()

def test_cancel_game_not_waiting(mock_get_game_by_id, mock_game_socket_manager, mock_finish_game):
    mock_get_game_by_id.return_value = {'players': ['0', 'Test_Player'], 'state': 'started', 'creator': 'Test_Player'}
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/cancel", json=request_data)

    assert response.status_code == 403
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_finish_game.assert_not_called()

def test_cancel_game_invalid_id(mock_get_game_by_id, mock_game_socket_manager, mock_finish_game):
    mock_get_game_by_id.side_effect = Exception("TEST")
    mock_game_socket_manager.broadcast_game = AsyncMock()

    request_data = {'player_id': 'Test_Player'}
    response = client.post("/games/Test_Game/cancel", json=request_data)

    assert response.status_code == 404
    mock_get_game_by_id.assert_called_once_with("Test_Game")
    mock_game_socket_manager.broadcast_game.assert_not_called()
    mock_finish_game.assert_not_called()


if __name__ == "__main__":
    pytest.main()
