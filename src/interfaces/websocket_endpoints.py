from fastapi import WebSocket, WebSocketDisconnect
from entities.game.game_utils import get_games_with_player_names, get_players_names, get_game_status, get_game_by_id
from interfaces.SocketManagers import public_manager, game_socket_manager

async def public_games(websocket: WebSocket):
    await public_manager.connect(websocket)
    print(f"Public WS Connections:\n {public_manager.connections}")
    try:
        games = get_games_with_player_names()
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

async def connect_game(websocket : WebSocket, game_id, player_id):
    if game_id in game_socket_manager.sockets_map:
        if player_id in game_socket_manager.sockets_map[game_id]:
            await game_socket_manager.user_connect(game_id, player_id, websocket)          
            if get_game_by_id(game_id)["state"] == "waiting":
                await websocket.send_json({"type":"SUCCESS","payload": get_players_names(game_id)})
            else:
                await websocket.send_json({"type":"GameStarted","payload": get_game_status(game_id)})
                
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                await game_socket_manager.user_disconnect(game_id, player_id)
        else:
            await websocket.accept()
            await websocket.send_json({"type":"ERROR","payload":"Invalid game_id or player_id"})
            await websocket.close()
            