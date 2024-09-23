# back/main.py

from fastapi import FastAPI, WebSocket
from interfaces import game_endpoints, websocket_interface
import uvicorn

app = FastAPI()

# Incluir todos los endpoints debajo de /games
app.include_router(game_endpoints.router, prefix="/games")

app.websocket("/games")(websocket_interface.public_games)

app.websocket("/games/{playerid}")(websocket_interface.in_game_connection)

# Levantar el server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)