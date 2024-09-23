from fastapi import WebSocket, WebSocketDisconnect
from entities.game.game_utils import get_listed_games
import json

open_websockets = []


async def public_games(websocket: WebSocket):
    await websocket.accept()
    open_websockets.append(websocket)
    print(open_websockets)
    while True:
        try:
            games = get_listed_games()
            games_listWS = {"type": "CreatedGames","payload": games}       
            await websocket.send_text(json.dumps(games_listWS))
        except WebSocketDisconnect:
            print("UserDisconnect - Close Connection")
            open_websockets.remove(websocket)
            break

