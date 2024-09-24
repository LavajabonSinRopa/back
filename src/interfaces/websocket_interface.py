from fastapi import WebSocket, WebSocketDisconnect
from entities.game.game_utils import get_listed_games

class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        
    async def disconnect(self, websocket: WebSocket):
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
    

public_manager = ConnectionManager()

async def public_games(websocket: WebSocket):
    await public_manager.connect(websocket)
    print(public_manager.connections)
    try:
        games = get_listed_games()
        games_listWS = {"type": "CreatedGames","payload": games} 
        await public_manager.send_personal_message(games_listWS, websocket)
    except WebSocketDisconnect:
        await public_manager.disconnect(websocket)
    
    while True:
        try:
            await websocket.receive_text() # En realidad no espera nada es solo para mantener el socket abierto
        except WebSocketDisconnect:
            await public_manager.disconnect(websocket)
            break
