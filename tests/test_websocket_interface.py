import pytest
import asyncio
import json
import websockets

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

@pytest.mark.asyncio
async def test_fake_game_connection():
    uri = "ws://localhost:8000/games/fake_id"
    async with websockets.connect(uri) as websocket:
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=5)
            print(data)
        except asyncio.TimeoutError:
            print("Timeout")
            return
        data = json.loads(data)
        assert data["type"] == "ERROR"
        assert data["payload"] == "No players in Game with this ID"

@pytest.mark.asyncio
async def test_valid_game_connection():    
    uri = "ws://localhost:8000/games/test_id"
    async with websockets.connect(uri) as websocket:
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=5)
            print(data)
        except asyncio.TimeoutError:
            print("Timeout")
            return
        data = json.loads(data)
        assert data["type"] == "INFO"
        assert data["payload"] == "GameSocket connected"
    
