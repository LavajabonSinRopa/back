# back/schemas/game_schemas.py

from pydantic import BaseModel

# Formato de POST a /games
class CreateGameRequest(BaseModel):
    game_name: str
    player_name: str
    password: str = ""
    

# Formato de respuesta de POST a /games
class CreateGameResponse(BaseModel):
    player_id: str
    game_id: str

# POST a /games/<game_id>/join
class JoinGameRequest(BaseModel):
    player_name: str
    password: str = ""

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

# POST a games/<game_id>/move
class MakeMoveRequest(BaseModel):
    player_id: str
    card_id: str
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    
class UnmakeMoveRequest(BaseModel):
    player_id: str
    
class applyTempMovementsRequest(BaseModel):
    player_id: str

class CompleteFigureRequest(BaseModel):
    player_id : str
    card_id : str
    x : int
    y : int

class BlockFigureRequest(BaseModel):
    player_id : str
    card_id : str
    x : int
    y : int