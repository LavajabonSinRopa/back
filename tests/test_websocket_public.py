import pytest
import asyncio
import json
import websockets
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from unittest.mock import Mock, AsyncMock
from interfaces.SocketManagers import PublicManager

#Run this test with server up

@pytest.mark.asyncio
async def test_public_connection():
    uri = "ws://localhost:8000/games"
    async with websockets.connect(uri) as websocket:
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=15)
            print(data)
        except asyncio.TimeoutError:
            print("Timeout")
            return
        data = json.loads(data)
        assert data["type"] == "CreatedGames"
        assert isinstance(data["payload"], list)

class MockWebSocket:
    def __init__(self):
        self.client_state = WebSocketState.CONNECTED
        self.accept = AsyncMock()
        self.close = AsyncMock()
        self.send_json = AsyncMock()

@pytest.fixture
def public_manager():
    return PublicManager()

@pytest.mark.asyncio
async def test_public_manager_connect(public_manager):
    ws = MockWebSocket()
    await public_manager.connect(ws)
    assert ws in public_manager.connections
    ws.accept.assert_called_once()

@pytest.mark.asyncio
async def test_public_manager_disconnect(public_manager):
    ws = MockWebSocket()
    public_manager.connections.append(ws)
    await public_manager.disconnect(ws)
    assert ws not in public_manager.connections
    ws.close.assert_called_once()

@pytest.mark.asyncio
async def test_public_manager_send_personal_message(public_manager):
    ws = MockWebSocket()
    message = {"type": "test", "content": "test message"}
    await public_manager.send_personal_message(message, ws)
    ws.send_json.assert_called_once_with(message)

@pytest.mark.asyncio
async def test_public_manager_broadcast(public_manager):
    ws1, ws2 = MockWebSocket(), MockWebSocket()
    public_manager.connections = [ws1, ws2]
    message = {"type": "broadcast", "content": "broadcast message"}
    await public_manager.broadcast(message)
    ws1.send_json.assert_called_once_with(message)
    ws2.send_json.assert_called_once_with(message)

@pytest.mark.asyncio
async def test_public_manager_send_personal_message_disconnect(public_manager):
    ws = MockWebSocket()
    ws.send_json.side_effect = WebSocketDisconnect()
    public_manager.disconnect = AsyncMock()
    
    message = {"type": "test", "content": "test message"}
    await public_manager.send_personal_message(message, ws)
    
    ws.send_json.assert_called_once_with(message)
    public_manager.disconnect.assert_called_once_with(ws)

@pytest.mark.asyncio
async def test_public_manager_broadcast_disconnect(public_manager):
    ws1, ws2 = MockWebSocket(), MockWebSocket()
    ws1.send_json.side_effect = WebSocketDisconnect()
    public_manager.connections = [ws1, ws2]
    public_manager.disconnect = AsyncMock()
    
    message = {"type": "broadcast", "content": "broadcast message"}
    await public_manager.broadcast(message)
    
    ws1.send_json.assert_called_once_with(message)
    ws2.send_json.assert_called_once_with(message)
    public_manager.disconnect.assert_called_once_with(ws1)
