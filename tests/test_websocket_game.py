import unittest
import requests
import asyncio
import websockets
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from interfaces.SocketManagers import game_socket_manager

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear juego y jugador
        URL = "http://localhost:8000/games"
        game_data = {"game_name": "Partida de 3", "player_name": "El Primero"}
        r = requests.post(URL, json=game_data, headers={"Content-Type": "application/json"})
        cls.game_id = r.json().get("game_id") # Guardas game_id
        cls.player1_id = r.json().get("player_id")  # Guardar player1_id 
        
        #Bucle de eventos
        
        cls.loop = asyncio.new_event_loop()
        #WS primer jugador
        
        cls.websocket_urls = [
            f"ws://localhost:8000/games/{cls.game_id}/{cls.player1_id}"
        ]
        
        # Une a un segundo jugador
        URL = f"http://localhost:8000/games/{cls.game_id}/join"
        player_data = {"player_name": "El segundo"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        cls.player2_id = r.json().get("player_id")
        
        #WS segundo jugador
        cls.websocket_urls.append(f"ws://localhost:8000/games/{cls.game_id}/{cls.player2_id}")
  
        #Conectar WS
        
        cls.websockets = []
        cls.loop.run_until_complete(cls.connect_websockets())

              
    @classmethod
    async def connect_websockets(cls):
        for url in cls.websocket_urls:
            websocket = await websockets.connect(url)
            cls.websockets.append(websocket)

    @classmethod
    async def close_websockets(cls):
        for websocket in cls.websockets:
            if websocket is not None:
                await websocket.close()

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(cls.close_websockets())
        cls.loop.close()

    def test1_websocket_first_receive(self):
        # Probar recepción del SUCCESS messagge
        async def receive_message(websocket):
            message = await websocket.recv()
            return message
        print("--First receive--")
        for websocket in self.websockets:
            message = self.loop.run_until_complete(receive_message(websocket))
            print(f"Received message: {message}")
            message_dict = json.loads(message) 
            self.assertEqual(message_dict, {"type":"SUCCESS","payload":"GameWS connected"})

    def test2_websocket_broadcast(self):
        # Probar broadcast por nuevo jugador

        URL = f"http://localhost:8000/games/{self.game_id}/join"
        player_data = {"player_name": "El Tercero"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        self.player3_id = r.json().get("player_id")
     

        broadcast_message = {"type":"PlayerJoined", "payload": "El Tercero"}
        
        async def receive_message(websocket):
            message = await websocket.recv()
            return message
        print("--Broadcast receive--")
        for websocket in self.websockets:
            message = self.loop.run_until_complete(receive_message(websocket))
            print(f"Received message: {message}")
            message_dict = json.loads(message) 
            self.assertEqual(message_dict, broadcast_message)


if __name__ == "__main__":
    unittest.main()