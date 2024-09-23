from fastapi import WebSocket, WebSocketDisconnect
from entities.game.game_utils import get_listed_games
import json
import asyncio
playersSockets = {}

async def public_games(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            games = get_listed_games()
            games_listWS = {"type": "CreatedGames","payload": games}       
            await websocket.send_json(games_listWS)
        except WebSocketDisconnect:
            print("UserDisconnect - Close Connection")
            break


async def in_game_connection(playerid: str, websocket: WebSocket):
    await websocket.accept()
    if not playerid in playersSockets:
        await websocket.send_json({"type": "ERROR", "payload": "No players in Game with this ID"})
    else:
        playersSockets[playerid] = websocket 
        while True:
            try:
                #Solo mantiene la conexión, los mensajes van por send_data_to_playerWS 
                await asyncio.sleep(1)
                print(playersSockets)
                pass
            except WebSocketDisconnect:
                print("UserDisconnect - Close Connection")
                break
            except KeyError:
                print("User hasnt game")



#TODO: TEST
async def send_data_to_playerWS(playerid:int,data: dict):
    try:
        await playersSockets[playerid].send_json(data)
    except WebSocketDisconnect:
        print("UserDisconnect - Cant send")
    except KeyError:
        print("User not connected")