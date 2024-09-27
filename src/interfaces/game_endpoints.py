# back/interfaces/game_endpoints.py

from fastapi import APIRouter, HTTPException
from entities.game.game import Game
from entities.game.game_utils import add_game, get_game_by_id
from entities.player.player import Player
from schemas.game_schemas import (CreateGameRequest, CreateGameResponse, 
                                  JoinGameRequest, JoinGameResponse)

router = APIRouter()

# POST a /games -- Crear partida. recibe JSON de tipo CreateGameRequest en el body
@router.post("")
def create_game(request: CreateGameRequest):
    """Endpoint to create a new game."""
    if request.game_name == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    # Crear player (creador de la partida) y partida
    creator = Player(name=request.player_name)
    game = Game(name=request.game_name, creator=creator)

    add_game(game)

    return CreateGameResponse(game_id=game.unique_id, player_id=creator.unique_id)

@router.post("/{game_id}/join", response_model=JoinGameResponse)
async def join_game(game_id: str, request: JoinGameRequest):
    """Endpoint to join a game."""
    game = get_game_by_id(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Invalid game ID")
    
    # Crear player, agregarlo al juego
    player = Player(name=request.player_name)
    game.add_player(player)  

    # Devolver ID unico de jugador para la partida
    return JoinGameResponse(player_id=player.unique_id)