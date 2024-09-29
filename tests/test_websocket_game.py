import unittest
import requests
import asyncio
import websockets
import sys
import os
import json
from src.entities.game.game_utils import get_game_by_id

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
            self.assertEqual(message_dict, {"type":"SUCCESS","payload":get_game_by_id(self.game_id)["players"]})

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

    def test3_websocket_broadcast(self):
        # Agregar player nuevo
        URL = f"http://localhost:8000/games/{self.game_id}/join"
        player_data = {"player_name": "El Cuarto"}
        r = requests.post(URL, json=player_data, headers={"Content-Type": "application/json"})
        player4_id = r.json().get("player_id")

        # WS para el player nuevo
        self.websocket_urls.append(f"ws://localhost:8000/games/{self.game_id}/{player4_id}")
        
        # Conectarse a su websocket
        self.loop.run_until_complete(self.connect_websockets())

        # Player nuevo abandona
        URL = f"http://localhost:8000/games/{self.game_id}/leave"
        leave_data = {"player_id": player4_id}
        r = requests.post(URL, json=leave_data, headers={"Content-Type": "application/json"})

        # Mensaje de PlayerLeft experado
        broadcast_message = {"type": "PlayerLeft", "payload": player4_id}
        
        # Esperar el expected message hasta potencial timeout
        # TODO: refactorear toda la clase para usar esta version de receive_message, pasar broadcast_message x param
        async def receive_message(websocket):
            try:
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1)  # Esperar 1 seg
                        message_dict = json.loads(message)
                        print(f"Received message: {message_dict}")
                        if message_dict == broadcast_message: 
                            return True # Devolver True si se recibe el mensaje esperado
                    except asyncio.TimeoutError:
                        print("Timeout waiting for message...") 
                        break  
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        return False
            except Exception as e:
                print(f"Error in receive_message: {e}")
                return False

        print("--Broadcast receive--")
        received_any = False
        for websocket in self.websockets:
            if websocket.open:
                # Devuelve True cuando llega el mensaje esperado
                received = self.loop.run_until_complete(receive_message(websocket))
                if received:
                    received_any = True
                    break
            else:
                print(f"WebSocket {websocket} cerrado!")

        self.assertTrue(received_any, f"No llegó el mensaje esperado: {broadcast_message}")


if __name__ == "__main__":
    unittest.main()