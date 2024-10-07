import unittest
import requests
import uuid
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main
from entities.game import game_utils
from entities.player import player_utils
from interfaces import SocketManagers

# Create a TestClient for the FastAPI app
client = TestClient(main.app)

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
    mock_add_game.assert_called_once_with(game_name="Test Game", creator_id='1')
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

# class TestJoinGameEndpoint(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Crear juego
#         URL = "http://localhost:8000/games"
#         game_data = {"game_name": "juego2", "player_name": "mi nombre"}
#         r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
#         assert r.status_code == 200  # (cls.assertEqual da error)
#         cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
#         cls.creator_id = r.json().get("player_id")  # Guardar game_id para otros tests
        
#     def test1_join_game_success(self):
#         # Joinear juego ya creado
#         URL = "http://localhost:8000/games/{game_id}/join".format(game_id=self.game_id)
#         player_data = {"player_name": "otro nombre"}
#         r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 200)

#     def test2_join_game_invalid_game_id(self):
#         # Joinear juego inválido
#         URL = "http://localhost:8000/games/{game_id}/join".format(game_id="invalid_game_id")
#         player_data = {"player_name": "otro nombre pero distinto"}
#         r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 404)

#     def test3_join_game_starded_game_id(self):
#         # Joinear juego empezado
#         URL_START = f"http://localhost:8000/games/{self.game_id}/start"
#         start_data = {"player_id": self.creator_id}
#         r = requests.post(URL_START, json=start_data, headers={"Content-Type": "application/json"})

#         URL = "http://localhost:8000/games/{game_id}/join".format(game_id=self.game_id)
#         player_data = {"player_name": "otro nombre"}
#         r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 403)

#     def test4_join_full_game(self):
#         URL = "http://localhost:8000/games"
#         game_data = {"game_name": "juego2", "player_name": "mi nombre"}
#         r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
#         assert r.status_code == 200  # (cls.assertEqual da error)
#         game_id = r.json().get("game_id")

#         # Ver cantidad de jugadores 
#         URL_GAME = f"http://localhost:8000/games/{game_id}"
#         r = requests.get(URL_GAME, headers={"Content-Type": "application/json"})
#         # Calcular cantidad de jugafores que faltan para llenar la partida
#         players_left = 4 - len(r.json().get("players")) 


#         for i in range(1, players_left+10):
#             # Agregar jugador nuevo
#             URL = f"http://localhost:8000/games/{game_id}/join"
#             player_data = {"player_name": f"otro nombre {i}"}
#             r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})

#             # Si la sala está llena, el request debe devolver 403 forbidden
#             if i >= players_left+1:
#                self.assertEqual(r.status_code, 403)
#             else:
#                self.assertEqual(r.status_code, 200)


# class TestLeaveGameEndpoint(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Crear un juego y joinear un jugador
#         game_data = {"game_name": "test_leave_game", "player_name": "player_1"}
#         r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
#         assert r.status_code == 200
#         cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
#         cls.creator_player_id = r.json().get("player_id")  # Guardar player_id del creador

#         # Join con otro jugador (Player_2)
#         URL_JOIN = f"http://localhost:8000/games/{cls.game_id}/join"
#         player_data = {"player_name": "player_2"}
#         r = requests.post(URL_JOIN, json=player_data, headers={"Content-Type": "application/json"})
#         cls.player_2_id = r.json().get("player_id")  # Guardar player_id del segundo jugador
#         assert r.status_code == 200

#     def test_leave_game_success(self):
#         # Ver que el segundo jugador puede abandonar el juego
#         URL_LEAVE = f"http://localhost:8000/games/{self.game_id}/leave"
#         leave_data = {"player_id": self.player_2_id}
#         r = requests.post(URL_LEAVE, json=leave_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 200)  # Debería devolver 200 OK

#         # Ver que el jugador ya no está en el juego
#         URL_GAMES = "http://localhost:8000/games/"
#         r = requests.get(URL_GAMES)
#         game_data = r.json()

#         # La lista de jugadores no debe contener el player_2_id
#         players_in_game = [game['players'] for game in game_data]
#         self.assertNotIn(self.player_2_id, players_in_game)  # El jugador debe haber sido removido

#     def test_leave_game_invalid_player_id(self):
#         # Intentar dejar el juego con un ID de jugador inválido
#         URL_LEAVE = f"http://localhost:8000/games/{self.game_id}/leave"
#         leave_data = {"player_id": "invalid_player_id"}
#         r = requests.post(URL_LEAVE, json=leave_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 404)  # Deberia devolver 404 Not Found

#     def test_leave_game_creator(self):
#         # Ver que el creador del juego no puede dejar el juego
#         URL_LEAVE = f"http://localhost:8000/games/{self.game_id}/leave"
#         leave_data = {"player_id": self.creator_player_id}
#         r = requests.post(URL_LEAVE, json=leave_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 403)  # Debería devolver 403 forbidden

#         # Conseguir IDs de jugadores en la partida
#         URL_GAMES = "http://localhost:8000/games/"
#         r = requests.get(URL_GAMES)
#         game_data = r.json()
#         players_in_game = [game['players'] for game in game_data if game["unique_id"] == self.game_id]

#         # Flattenear la lista para que assertIn no compare las sublistas de players_in_game con el ID
#         players_in_game_flat = [item for sublist in players_in_game for item in sublist]
#         self.assertIn(self.creator_player_id, players_in_game_flat) # Verificar que el creador sigue en la partida

# class TestSkipTurnGameEndpoint(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Crear un juego y joinear un jugador
#         game_data = {"game_name": "test_leave_game", "player_name": "player_1"}
#         r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
#         assert r.status_code == 200
#         cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
#         cls.creator_player_id = r.json().get("player_id")  # Guardar player_id del creador

#         # Join con otro jugador (Player_2)
#         URL_JOIN = f"http://localhost:8000/games/{cls.game_id}/join"
#         player_data = {"player_name": "player_2"}
#         r = requests.post(URL_JOIN, json=player_data, headers={"Content-Type": "application/json"})
#         cls.player_2_id = r.json().get("player_id")  # Guardar player_id del segundo jugador
#         assert r.status_code == 200

#         #TODO: start game

#     def test_skip_turn_in_game(self):
#         URL_SKIP = f"http://localhost:8000/games/{self.game_id}/skip"
#         leave_data = {"player_id": self.player_2_id}
#         r1 = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
#         leave_data = {"player_id": self.creator_player_id}
#         r2 = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
#         #atleast one must have skipped turn
#         assert r1.status_code == 200 or r2.status_code == 200
#         r2 = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
#         #attemped to skip same player twice, must receive error message on the second attempt
#         assert r2.status_code >= 400
    
#     def test_skip_turn_not_in_game(self):
#         URL_SKIP = f"http://localhost:8000/games/{self.game_id}/skip"
#         leave_data = {"player_id": "NOESTOY"}
#         r = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
#         assert r.status_code >= 400

# class TestGetGameEndpoint(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.URL_GAMES = "http://localhost:8000/games"
#         cls.valid_game_data = {"game_name": "test_game", "player_name": "player_1"}

#         # Crear juego
#         r = requests.post(cls.URL_GAMES, json=cls.valid_game_data, headers={"Content-Type": "application/json"})
#         assert r.status_code == 200
#         cls.game_id = r.json().get("game_id")  # Guardar game_id

#     def test_GET_GAME_SUCCESS(self):
#         # Obtener datos del juego
#         URL = f"{self.URL_GAMES}/{self.game_id}"
#         r = requests.get(URL)
#         self.assertEqual(r.status_code, 200)
#         game_data = r.json()
#         self.assertEqual(game_data['name'], self.valid_game_data['game_name'])  # Verificar nombre

#     def test_GET_GAME_INVALID_ID(self):
#         # Obtener datos del juego con ID invalido
#         URL = f"{self.URL_GAMES}/invalid_game_id"
#         r = requests.get(URL)
#         self.assertEqual(r.status_code, 404)  # Debería devolver 404
#         self.assertIn("Invalid game ID", r.text)  # Verificar mensaje de error


# class TestStartGameEndpoint(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Crear un juego y joinear un jugador
#         game_data = {"game_name": "test_leave_game", "player_name": "player_1"}
#         r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
#         assert r.status_code == 200
#         cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
#         cls.creator_player_id = r.json().get("player_id")  # Guardar player_id del creador

#         # Join con otro jugador (Player_2)
#         URL_JOIN = f"http://localhost:8000/games/{cls.game_id}/join"
#         player_data = {"player_name": "player_2"}
#         r = requests.post(URL_JOIN, json=player_data, headers={"Content-Type": "application/json"})
#         cls.player_2_id = r.json().get("player_id")  # Guardar player_id del segundo jugador
#         assert r.status_code == 200

#     def test_start_game(self):
#         # Verificar que el juego se inicia correctamente
#         URL_START = f"http://localhost:8000/games/{self.game_id}/start"
#         start_data = {"player_id": self.creator_player_id}
#         r = requests.post(URL_START, json=start_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 200)
#     def test_start_invalid_player(self):
#         # Verificar que el juego no se inicia correctamente
#         URL_START = f"http://localhost:8000/games/{self.game_id}/start"
#         start_data = {"player_id": "invalid_id"}
#         r = requests.post(URL_START, json=start_data, headers={"Content-Type": "application/json"})
#         self.assertEqual(r.status_code, 403)


if __name__ == "__main__":
    unittest.main()