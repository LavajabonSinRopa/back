import unittest
import requests
from src.entities.game.game_utils import delete_all

URL = "http://localhost:8000/games"
game_data = {"game_name": "juego1", "player_name": "mi nombre"}
NofGamesCreated = 3

#Run this test with server up
class test_game_endpoints(unittest.TestCase):    
    def test_create_game_endpoint_success(self):
        delete_all()
        for _ in range(NofGamesCreated):
            r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
            assert r.status_code == 200
    def test_create_game_endpoint_failure(self):
        r = requests.post(URL, data=game_data, headers={"Content-Type": "application/json"})
        #mando un json malformado y checkeo que devuelva un codigo de error, cuando definamos El codigo de error exacto que queremos acá podemos checquear ese
        assert r.status_code >= 400
    def test_get_games_endpoint(self):
        r = requests.get(URL)
        assert r.status_code == 200
        #TODO: testear si los nombres returneados son correctos

class TestJoinGameEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear juego
        URL = "http://localhost:8000/games"
        game_data = {"game_name": "juego2", "player_name": "mi nombre"}
        r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
        assert r.status_code == 200  # (cls.assertEqual da error)
        cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests

    def test1_join_game_success(self):
        # Joinear juego ya creado
        URL = "http://localhost:8000/games/{game_id}/join".format(game_id=self.game_id)
        player_data = {"player_name": "otro nombre"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 200)

    def test2_join_game_invalid_game_id(self):
        # Joinear juego inválido
        URL = "http://localhost:8000/games/{game_id}/join".format(game_id="invalid_game_id")
        player_data = {"player_name": "otro nombre pero distinto"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 404)

    def test3_join_game_starded_game_id(self):
        # Joinear juego empezado
        URL_START = f"http://localhost:8000/games/{self.game_id}/start"
        start_data = {"player_id": self.creator_id}
        r = requests.post(URL_START, json=start_data, headers={"Content-Type": "application/json"})

        URL = "http://localhost:8000/games/{game_id}/join".format(game_id=self.game_id)
        player_data = {"player_name": "otro nombre"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 403)


class TestLeaveGameEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear un juego y joinear un jugador
        game_data = {"game_name": "test_leave_game", "player_name": "player_1"}
        r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
        assert r.status_code == 200
        cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
        cls.creator_player_id = r.json().get("player_id")  # Guardar player_id del creador

        # Join con otro jugador (Player_2)
        URL_JOIN = f"http://localhost:8000/games/{cls.game_id}/join"
        player_data = {"player_name": "player_2"}
        r = requests.post(URL_JOIN, json=player_data, headers={"Content-Type": "application/json"})
        cls.player_2_id = r.json().get("player_id")  # Guardar player_id del segundo jugador
        assert r.status_code == 200

    def test_leave_game_success(self):
        # Ver que el segundo jugador puede abandonar el juego
        URL_LEAVE = f"http://localhost:8000/games/{self.game_id}/leave"
        leave_data = {"player_id": self.player_2_id}
        r = requests.post(URL_LEAVE, json=leave_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 200)  # Debería devolver 200 OK

        # Ver que el jugador ya no está en el juego
        URL_GAMES = "http://localhost:8000/games/"
        r = requests.get(URL_GAMES)
        game_data = r.json()

        # La lista de jugadores no debe contener el player_2_id
        players_in_game = [game['players'] for game in game_data]
        print(players_in_game)
        self.assertNotIn(self.player_2_id, players_in_game)  # El jugador debe haber sido removido

    def test_leave_game_invalid_player_id(self):
        # Intentar dejar el juego con un ID de jugador inválido
        URL_LEAVE = f"http://localhost:8000/games/{self.game_id}/leave"
        leave_data = {"player_id": "invalid_player_id"}
        r = requests.post(URL_LEAVE, json=leave_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 404)  # Deberia devolver 404 Not Found

    def test_leave_game_creator(self):
        # Ver que el creador del juego no puede dejar el juego
        URL_LEAVE = f"http://localhost:8000/games/{self.game_id}/leave"
        leave_data = {"player_id": self.creator_player_id}
        r = requests.post(URL_LEAVE, json=leave_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 403)  # Debería devolver 403 forbidden

        # Conseguir IDs de jugadores en la partida
        URL_GAMES = "http://localhost:8000/games/"
        r = requests.get(URL_GAMES)
        game_data = r.json()
        players_in_game = [game['players'] for game in game_data if game["unique_id"] == self.game_id]

        # Flattenear la lista para que assertIn no compare las sublistas de players_in_game con el ID
        players_in_game_flat = [item for sublist in players_in_game for item in sublist]
        self.assertIn(self.creator_player_id, players_in_game_flat) # Verificar que el creador sigue en la partida

class TestSkipTurnGameEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear un juego y joinear un jugador
        game_data = {"game_name": "test_leave_game", "player_name": "player_1"}
        r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
        assert r.status_code == 200
        cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
        cls.creator_player_id = r.json().get("player_id")  # Guardar player_id del creador

        # Join con otro jugador (Player_2)
        URL_JOIN = f"http://localhost:8000/games/{cls.game_id}/join"
        player_data = {"player_name": "player_2"}
        r = requests.post(URL_JOIN, json=player_data, headers={"Content-Type": "application/json"})
        cls.player_2_id = r.json().get("player_id")  # Guardar player_id del segundo jugador
        assert r.status_code == 200

        #TODO: start game

    def test_skip_turn_in_game(self):
        URL_SKIP = f"http://localhost:8000/games/{self.game_id}/skip"
        leave_data = {"player_id": self.player_2_id}
        r1 = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
        leave_data = {"player_id": self.creator_player_id}
        r2 = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
        #atleast one must have skipped turn
        assert r1.status_code == 200 or r2.status_code == 200
        r2 = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
        #attemped to skip same player twice, must receive error message on the second attempt
        assert r2.status_code >= 400
    
    def test_skip_turn_not_in_game(self):
        URL_SKIP = f"http://localhost:8000/games/{self.game_id}/skip"
        leave_data = {"player_id": "NOESTOY"}
        r = requests.post(URL_SKIP, json=leave_data, headers={"Content-Type": "application/json"})
        assert r.status_code >= 400

class TestGetGameEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.URL_GAMES = "http://localhost:8000/games"
        cls.valid_game_data = {"game_name": "test_game", "player_name": "player_1"}

        # Crear juego
        r = requests.post(cls.URL_GAMES, json=cls.valid_game_data, headers={"Content-Type": "application/json"})
        assert r.status_code == 200
        cls.game_id = r.json().get("game_id")  # Guardar game_id

    def test_GET_GAME_SUCCESS(self):
        # Obtener datos del juego
        URL = f"{self.URL_GAMES}/{self.game_id}"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)
        game_data = r.json()
        print(game_data)
        print(self.valid_game_data)
        self.assertEqual(game_data['name'], self.valid_game_data['game_name'])  # Verificar nombre

    def test_GET_GAME_INVALID_ID(self):
        # Obtener datos del juego con ID invalido
        URL = f"{self.URL_GAMES}/invalid_game_id"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 404)  # Debería devolver 404
        self.assertIn("Invalid game ID", r.text)  # Verificar mensaje de error


class TestStartGameEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear un juego y joinear un jugador
        game_data = {"game_name": "test_leave_game", "player_name": "player_1"}
        r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
        assert r.status_code == 200
        cls.game_id = r.json().get("game_id")  # Guardar game_id para otros tests
        cls.creator_player_id = r.json().get("player_id")  # Guardar player_id del creador

        # Join con otro jugador (Player_2)
        URL_JOIN = f"http://localhost:8000/games/{cls.game_id}/join"
        player_data = {"player_name": "player_2"}
        r = requests.post(URL_JOIN, json=player_data, headers={"Content-Type": "application/json"})
        cls.player_2_id = r.json().get("player_id")  # Guardar player_id del segundo jugador
        assert r.status_code == 200

    def test_start_game(self):
        # Verificar que el juego se inicia correctamente
        URL_START = f"http://localhost:8000/games/{self.game_id}/start"
        start_data = {"player_id": self.creator_player_id}
        r = requests.post(URL_START, json=start_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 200)
    def test_start_invalid_player(self):
        # Verificar que el juego no se inicia correctamente
        URL_START = f"http://localhost:8000/games/{self.game_id}/start"
        start_data = {"player_id": "invalid_id"}
        r = requests.post(URL_START, json=start_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 403)


if __name__ == "__main__":
    unittest.main()