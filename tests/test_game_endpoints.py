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

if __name__ == "__main__":
    unittest.main()