# back/schemas/game_schemas.py

from pydantic import BaseModel
from typing import List

# Formato de POST a /games
class CreateGameRequest(BaseModel):
    game_name: str
    player_name: str

# Formato de respuesta de POST a /games
class CreateGameResponse(BaseModel):
    player_id: str
    game_id: str

class GameInResponse(BaseModel):
    game_id: str
    game_name: str
