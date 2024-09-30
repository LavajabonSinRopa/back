from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from entities.game.game_utils import get_games


## Clase que se encarga de las conexiones publicas
class PublicManager:
    def __init__(self):
        self.connections: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        
    async def disconnect(self, websocket: WebSocket):
        if websocket is not None:
            websocket.close()
        
        if websocket in self.connections:
            self.connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except WebSocketDisconnect:
            await self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                await self.disconnect(connection)
    
    
    
#Clase que se encarga de las conexiones privadas por partida
class GameSocketManager:
    def __init__(self):
        self.sockets_map = {"game_idTEST":{"player_idTEST" : None}}
        for game in get_games():
            game_id = game["unique_id"]
            if game_id not in self.sockets_map:
                self.sockets_map[game_id] = {}
            for player in game['players']:
                self.sockets_map[game_id][player] = None
        print(f"SOCKETS_MAP--{self.sockets_map}--SOCKETS_MAP")
    
    def create_game_map(self,game_id):
        if game_id not in self.sockets_map:
            self.sockets_map[game_id] = {}
    
    def join_player_to_game_map(self,game_id,player_id):
        if player_id not in self.sockets_map[game_id]:
            self.sockets_map[game_id][player_id] = None
    
    async def broadcast_game(self, game_id: str, message: dict):
        for player in self.sockets_map[game_id]:
            if self.sockets_map[game_id][player] is not None:
                try:
                    await self.sockets_map[game_id][player].send_json(message)
                except Exception as e:
                    print(f"Error sending message to player {player}: {e}")
             
    async def send_to_user(self, game_id, player_id, message):
        if game_id in self.sockets_map and player_id in self.sockets_map[game_id]:
            websocket = self.sockets_map[game_id][player_id]
            if websocket is not None and websocket.client_state is WebSocketState.CONNECTED:
                await websocket.send_json(message)
            else:
                print(f"WebSocket for player {player_id} in game {game_id} is not connected.")
        else:
            print(f"Game ID {game_id} or Player ID {player_id} not found in sockets_map.")
      
    async def user_connect(self, game_id: str, player_id: str, websocket: WebSocket):
        try:
            await websocket.accept()
            self.sockets_map[game_id][player_id] = websocket
        except Exception as e:
            print(f"Error accepting connection for player {player_id}: {e}")

    async def user_disconnect(self,game_id,player_id):
        if self.sockets_map[game_id][player_id] != None and self.sockets_map[game_id][player_id].client_state is WebSocketState.CONNECTED:
            await self.sockets_map[game_id][player_id].close()
        self.sockets_map[game_id][player_id] = None
        
        
    async def clean_game(self, game_id):
        if game_id in self.sockets_map:
            await self.broadcast_game(game_id, {"type": "GameClosed", "payload": "Game Closed, disconnected"})
        
            for player_id, websocket in self.sockets_map[game_id].items():
                if websocket is WebSocketState.CONNECTED:
                    await websocket.close()
            del self.sockets_map[game_id]
    
    # Imprimir el estado actual de sockets_map
        print(f"SOCKETS_MAP--{self.sockets_map}--SOCKETS_MAP")





public_manager = PublicManager()

game_socket_manager = GameSocketManager()