import unittest
import requests

#Run this test with server up
class test_game_endpoints(unittest.TestCase):
    def test_create_game_endpoint(self):
        URL = "http://localhost:8000/games"
        game_data = {"game_name": "juego1", "player_name": "mi nombre"}
        r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
        assert r.status_code == 200

if __name__ == "__main__":
    unittest.main()