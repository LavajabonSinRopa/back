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

class GameInResponse(BaseModel):
    game_id: str
    game_name: str

# POST a games/<game_id>/leave
class LeaveGameRequest(BaseModel):
    player_id: str

class SkipTurnRequest(BaseModel):
    player_id: str
    
 # POST a games/<game_id>/start   
class StartGameResponse(BaseModel):
    player_id: str