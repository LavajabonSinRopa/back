# back/main.py

from fastapi import FastAPI
from interfaces import game_endpoints
import uvicorn

app = FastAPI()

# Incluir todos los endpoints debajo de /games
app.include_router(game_endpoints.router, prefix="/games")

# Levantar el server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)