import sys
import os
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi import WebSocket, WebSocketDisconnect

# Añadir el directorio 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from interfaces.websocket_endpoints import public_games, connect_game

@pytest.mark.asyncio
async def test_public_games():
    websocket = AsyncMock(spec=WebSocket)
    websocket.receive_text = AsyncMock(side_effect=WebSocketDisconnect)
    
    with patch('interfaces.websocket_endpoints.public_manager') as mock_public_manager, \
         patch('interfaces.websocket_endpoints.get_games_with_player_names') as mock_get_games:
        
        mock_public_manager.connect = AsyncMock()
        mock_public_manager.disconnect = AsyncMock()
        mock_public_manager.send_personal_message = AsyncMock()
        mock_get_games.return_value = [{"game_id": "1", "players": ["Player1", "Player2"]}]
        
        try:
            await asyncio.wait_for(public_games(websocket), timeout=1.0)
        except asyncio.TimeoutError:
            pass
        
        mock_public_manager.connect.assert_called_once_with(websocket)
        mock_public_manager.send_personal_message.assert_called_once_with(
            {"type": "CreatedGames", "payload": [{"game_id": "1", "players": ["Player1", "Player2"]}]},
            websocket
        )
        mock_public_manager.disconnect.assert_called_once_with(websocket)

@pytest.mark.asyncio
async def test_connect_game_waiting():
    websocket = AsyncMock(spec=WebSocket)
    game_id = "test_game_id"
    player_id = "test_player_id"
    
    with patch('interfaces.websocket_endpoints.game_socket_manager') as mock_game_socket_manager, \
         patch('interfaces.websocket_endpoints.get_game_by_id') as mock_get_game_by_id, \
         patch('interfaces.websocket_endpoints.get_players_names') as mock_get_players_names, \
         patch('interfaces.websocket_endpoints.get_game_status') as mock_get_game_status, \
         patch('interfaces.websocket_endpoints.get_player_name') as mock_get_player_name:
        
        
        websocket.receive_text = AsyncMock(side_effect=[None, WebSocketDisconnect])
        mock_game_socket_manager.sockets_map = {game_id: {player_id: websocket}}
        mock_game_socket_manager.user_connect = AsyncMock()
        mock_game_socket_manager.user_disconnect = AsyncMock()
        mock_game_socket_manager.broadcast_game = AsyncMock()
        mock_get_game_by_id.return_value = {"state": "waiting"}
        mock_get_players_names.return_value = ["Player1", "Player2"]
        mock_get_game_status.return_value = {"status": "lorem ipsum"}
        mock_get_player_name.return_value = "Player1"
        
        await connect_game(websocket, game_id, player_id)
        
        mock_game_socket_manager.user_connect.assert_called_once_with(game_id, player_id, websocket)
        websocket.send_json.assert_called_with({"type": "SUCCESS", "payload": ["Player1", "Player2"]})
        

@pytest.mark.asyncio
async def test_connect_game_started():
    websocket = AsyncMock(spec=WebSocket)
    game_id = "test_game_id"
    player_id = "test_player_id"
    
    with patch('interfaces.websocket_endpoints.game_socket_manager') as mock_game_socket_manager, \
         patch('interfaces.websocket_endpoints.get_game_by_id') as mock_get_game_by_id, \
         patch('interfaces.websocket_endpoints.get_players_names') as mock_get_players_names, \
         patch('interfaces.websocket_endpoints.get_game_status') as mock_get_game_status, \
         patch('interfaces.websocket_endpoints.get_player_name') as mock_get_player_name:
        
        
        websocket.receive_text = AsyncMock(side_effect=[None, WebSocketDisconnect])
        mock_game_socket_manager.sockets_map = {game_id: {player_id: websocket}}
        mock_game_socket_manager.user_connect = AsyncMock()
        mock_game_socket_manager.user_disconnect = AsyncMock()
        mock_game_socket_manager.broadcast_game = AsyncMock()
        mock_get_game_by_id.return_value = {"state": "started"}
        mock_get_players_names.return_value = ["Player1", "Player2"]
        mock_get_game_status.return_value = "lorem ipsum"
        mock_get_player_name.return_value = "Player1"
        
        await connect_game(websocket, game_id, player_id)
        
        mock_game_socket_manager.user_connect.assert_called_once_with(game_id, player_id, websocket)
        websocket.send_json.assert_called_with({"type":"GameStarted","payload": "lorem ipsum"})

@pytest.mark.asyncio
async def test_connect_game_bad_game_id():
    websocket = AsyncMock(spec=WebSocket)
    game_id = "invalid_game_id"
    player_id = "test_player_id"
    
    with patch('interfaces.websocket_endpoints.game_socket_manager') as mock_game_socket_manager:
        mock_game_socket_manager.sockets_map = {}
        
        await connect_game(websocket, game_id, player_id)
        
        websocket.accept.assert_called_once()
        websocket.send_json.assert_called_once_with({"type": "ERROR", "payload": "Invalid game_id"})
        websocket.close.assert_called_once()
        
@pytest.mark.asyncio
async def test_connect_game_bad_player_id():
    websocket = AsyncMock(spec=WebSocket)
    game_id = "test_game_id"
    player_id = "bad_player_id"
    
    with patch('interfaces.websocket_endpoints.game_socket_manager') as mock_game_socket_manager:
        mock_game_socket_manager.sockets_map = {game_id: {}}
        
        await connect_game(websocket, game_id, player_id)
        
        websocket.accept.assert_called_once()
        websocket.send_json.assert_called_once_with({"type": "ERROR", "payload": "Invalid player_id"})
        websocket.close.assert_called_once()



@pytest.mark.asyncio
async def test_send_message():
    websocket = AsyncMock(spec=WebSocket)
    game_id = "test_game_id"
    player_id = "test_player_id"
    
    with patch('interfaces.websocket_endpoints.game_socket_manager') as mock_game_socket_manager, \
         patch('interfaces.websocket_endpoints.get_game_by_id') as mock_get_game_by_id, \
         patch('interfaces.websocket_endpoints.get_players_names') as mock_get_players_names, \
         patch('interfaces.websocket_endpoints.get_game_status') as mock_get_game_status, \
         patch('interfaces.websocket_endpoints.get_player_name') as mock_get_player_name, \
         patch('interfaces.websocket_endpoints.datetime') as mock_datetime:
        
        websocket.receive_text = AsyncMock(side_effect=["Hola", WebSocketDisconnect])
        mock_game_socket_manager.sockets_map = {game_id: {player_id: websocket}}
        mock_game_socket_manager.user_connect = AsyncMock()
        mock_game_socket_manager.user_disconnect = AsyncMock()
        mock_game_socket_manager.broadcast_game = AsyncMock()
        mock_get_game_by_id.return_value = {"state": "waiting"}
        mock_get_players_names.return_value = ["Player1", "Player2"]
        mock_get_game_status.return_value = {"status": "ongoing"}
        mock_get_player_name.return_value = "Player1"
        mock_datetime.datetime.now.return_value.strftime.return_value = "12:00:00"
        await connect_game(websocket, game_id, player_id)
        
        mock_game_socket_manager.broadcast_game.assert_called_with(
            game_id,
            {"type": "ChatMessage", "payload": {"time": "12:00:00", "player_name": "Player1", "player_id": "test_player_id", "message": "Hola"}}
        )
        
        mock_game_socket_manager.user_disconnect.assert_called_once_with(game_id, player_id)






if __name__ == "__main__":
    pytest.main()