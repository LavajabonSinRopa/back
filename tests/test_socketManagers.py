import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from interfaces.SocketManagers import PublicManager
from interfaces.SocketManagers import GameSocketManager
@pytest.mark.asyncio
async def test_public_connect():
    manager = PublicManager()
    websocket = AsyncMock(spec=WebSocket)
    
    await manager.connect(websocket)
    
    websocket.accept.assert_called_once()
    assert websocket in manager.connections

@pytest.mark.asyncio
async def test_public_disconnect():
    manager = PublicManager()
    websocket = AsyncMock(spec=WebSocket)
    
    await manager.connect(websocket)
    await manager.disconnect(websocket)
    
    websocket.close.assert_called_once()
    assert websocket not in manager.connections

@pytest.mark.asyncio
async def test_public_send_personal_message():
    manager = PublicManager()
    websocket = AsyncMock(spec=WebSocket)
    
    await manager.connect(websocket)
    message = {"type": "test", "payload": "data"}
    
    await manager.send_personal_message(message, websocket)
    
    websocket.send_json.assert_called_once_with(message)
    assert websocket in manager.connections

@pytest.mark.asyncio
async def test_public_send_personal_message_disconnect():
    manager = PublicManager()
    websocket = AsyncMock(spec=WebSocket)
    
    await manager.connect(websocket)
    message = {"type": "test", "payload": "data"}
    
    websocket.send_json = AsyncMock(side_effect=WebSocketDisconnect)
    
    await manager.send_personal_message(message, websocket)
    
    websocket.send_json.assert_called_once_with(message)
    websocket.close.assert_called_once()
    assert websocket not in manager.connections

@pytest.mark.asyncio
async def test_public_broadcast():
    manager = PublicManager()
    websocket1 = AsyncMock(spec=WebSocket)
    websocket2 = AsyncMock(spec=WebSocket)
    
    await manager.connect(websocket1)
    await manager.connect(websocket2)
    message = {"type": "broadcast", "payload": "data"}
    
    await manager.broadcast(message)
    
    websocket1.send_json.assert_called_once_with(message)
    websocket2.send_json.assert_called_once_with(message)
    
@pytest.fixture
def game_socket_manager():
    with patch('interfaces.SocketManagers.get_all_games', return_value=[
        {"unique_id": "game_id1", "players": ["player1", "player2"]},
        {"unique_id": "game_id2", "players": ["player3", "player4"]}
    ]):
        return GameSocketManager()

@pytest.mark.asyncio
async def test_create_game_map(game_socket_manager):
    game_id = "new_game_id"
    game_socket_manager.create_game_map(game_id)
    assert game_id in game_socket_manager.sockets_map
    assert game_socket_manager.sockets_map[game_id] == {}

@pytest.mark.asyncio
async def test_join_player_to_game_map(game_socket_manager):
    game_id = "game_id1"
    player_id = "new_player_id"
    game_socket_manager.join_player_to_game_map(game_id, player_id)
    assert player_id in game_socket_manager.sockets_map[game_id]
    assert game_socket_manager.sockets_map[game_id][player_id] is None

@pytest.mark.asyncio
async def test_broadcast_game(game_socket_manager):
    game_id = "game_id1"
    player_id = "player1"
    websocket = AsyncMock(spec=WebSocket)
    game_socket_manager.sockets_map[game_id][player_id] = websocket
    message = {"type": "broadcast", "payload": "data"}
    
    await game_socket_manager.broadcast_game(game_id, message)
    
    websocket.send_json.assert_called_once_with(message)

@pytest.mark.asyncio
async def test_broadcast_game_disconnect(game_socket_manager):
    game_id = "game_id1"
    player_id = "player1"
    websocket = AsyncMock(spec=WebSocket)
    game_socket_manager.sockets_map[game_id][player_id] = websocket
    message = {"type": "broadcast", "payload": "data"}
    
    websocket.send_json = AsyncMock(side_effect=WebSocketDisconnect)
    
    await game_socket_manager.broadcast_game(game_id, message)
    
    websocket.send_json.assert_called_once_with(message)

@pytest.mark.asyncio
async def test_send_to_user(game_socket_manager):
    game_id = "game_id1"
    player_id = "player1"
    websocket = AsyncMock(spec=WebSocket)
    websocket.client_state = WebSocketState.CONNECTED
    game_socket_manager.sockets_map[game_id][player_id] = websocket
    message = {"type": "broadcast", "payload": "data"}
    
    await game_socket_manager.send_to_user(game_id, player_id, message)
    
    websocket.send_json.assert_called_once_with(message)
    
@pytest.mark.asyncio
async def test_user_connect(game_socket_manager):
    game_id = "game_id1"
    player_id = "player1"
    websocket = AsyncMock(spec=WebSocket)
    
    await game_socket_manager.user_connect(game_id, player_id, websocket)
        
    assert game_socket_manager.sockets_map[game_id][player_id] == websocket

@pytest.mark.asyncio
async def test_user_disconnect(game_socket_manager):
    game_id = "game_id1"
    player_id = "player1"
    websocket = AsyncMock(spec=WebSocket)
    websocket.client_state = WebSocketState.CONNECTED
    game_socket_manager.sockets_map[game_id][player_id] = websocket
    
    await game_socket_manager.user_disconnect(game_id, player_id)
    
    websocket.close.assert_called_once()
    assert game_socket_manager.sockets_map[game_id][player_id] is None

@pytest.mark.asyncio
async def test_clean_game(game_socket_manager):
    game_id = "game_id1"
    player1_id = "player1"
    player2_id = "player2"
    websocket = AsyncMock(spec=WebSocket)
    websocket2 = AsyncMock(spec=WebSocket)
    websocket.client_state = WebSocketState.CONNECTED
    websocket2.client_state = WebSocketState.CONNECTED 
    game_socket_manager.sockets_map[game_id][player1_id] = websocket
    game_socket_manager.sockets_map[game_id][player2_id] = websocket2
    
    await game_socket_manager.clean_game(game_id)
    
    websocket.close.assert_called_once()
    websocket2.close.assert_called_once()
    assert game_socket_manager.sockets_map.get(game_id) is None



if __name__ == "__main__":
    pytest.main()