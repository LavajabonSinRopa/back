import asyncio
import json
import websockets

async def test_websocket_connection():
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

if __name__ == "__main__":
    asyncio.run(test_websocket_connection())