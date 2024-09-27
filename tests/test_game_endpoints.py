import unittest
import requests

URL = "http://localhost:8000/games"
game_data = {"game_name": "juego1", "player_name": "mi nombre"}
NofGamesCreated = 1007

#Run this test with server up
class test_game_endpoints(unittest.TestCase):        
    def test_create_game_endpoint_success(self):
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
        res = r.json()
        assert len(res) == NofGamesCreated
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

    def test_join_game_success(self):
        # Joinear juego ya creado
        URL = "http://localhost:8000/games/{game_id}/join".format(game_id=self.game_id)
        player_data = {"player_name": "otro nombre"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 200)

    def test_join_game_invalid_game_id(self):
        # Joinear juego inválido
        URL = "http://localhost:8000/games/{game_id}/join".format(game_id="invalid_game_id")
        player_data = {"player_name": "otro nombre pero distinto"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 404)



if __name__ == "__main__":
    unittest.main()