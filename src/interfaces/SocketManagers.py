from fastapi import WebSocket, WebSocketDisconnect
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
    def __init__(self) -> None:
        self.sockets_map = {}
        for game in get_games():
            game_id = game["unique_id"]
            if game_id not in self.sockets_map:
                self.sockets_map[game_id] = {}
            for player in game['players']:
                self.sockets_map[game_id][player] = None
        print(f"SOCKET_MAP--{self.sockets_map}--SOCKET_MAP")
    
    async def broadcast_game(self, game_id: str, message: dict) -> None:
        for player in self.sockets_map[game_id]:
            if self.sockets_map[game_id][player] is not None:
                try:
                    await self.sockets_map[game_id][player].send_json(message)
                except Exception as e:
                    print(f"Error sending message to player {player}: {e}")
             
    async def send_to_user(self, game_id: str, player_id: str, message: dict) -> None:
        if self.sockets_map[game_id][player_id] is not None:
            try:
                await self.sockets_map[game_id][player_id].send_json(message)
            except Exception as e:
                print(f"Error sending message to player {player_id}: {e}")
            
    async def user_connect(self, game_id: str, player_id: str, websocket: WebSocket) -> None:
        try:
            await websocket.accept()
            self.sockets_map[game_id][player_id] = websocket
            print(self.sockets_map)
        except Exception as e:
            print(f"Error accepting connection for player {player_id}: {e}")

    async def user_disconnect(self,game_id,player_id):
        if game_id in self.sockets_map and player_id in self.sockets_map[game_id]:
            if self.sockets_map[game_id][player_id] is not None:
                 await self.sockets_map[game_id][player_id].close()
            self.sockets_map[game_id][player_id] = None
            print(f"SOCKET_MAP--{self.sockets_map}--SOCKET_MAP")
        
    async def clean_game(self, game_id):
        if game_id in self.sockets_map:
            for player_id, websocket in self.sockets_map[game_id].items():
                if websocket is not None:
                    await websocket.close()
            del self.sockets_map[game_id]
        print(f"SOCKET_MAP--{self.sockets_map}--SOCKET_MAP")






public_manager = PublicManager()

game_socket_manager = GameSocketManager()