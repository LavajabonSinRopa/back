# back/schemas/game_schemas.py

from pydantic import BaseModel

# Formato de POST a /games
class CreateGameRequest(BaseModel):
    game_name: str
    player_name: str

# Formato de respuesta de POST a /games
class CreateGameResponse(BaseModel):
    player_id: str
    game_id: str

# POST a /games/<game_id>/join
class JoinGameRequest(BaseModel):
    player_name: str

# Respuesta de POST a games/<game_id>/join
class JoinGameResponse(BaseModel):
    player_id: str