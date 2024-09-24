# back/interfaces/game_endpoints.py

from fastapi import APIRouter, HTTPException
from entities.game.game import Game
from entities.game.game_utils import add_game, get_listed_games
from entities.player.player import Player
from schemas.game_schemas import CreateGameRequest, CreateGameResponse
from interfaces.websocket_interface import public_manager
router = APIRouter()

# POST a /games -- Crear partida. recibe JSON de tipo CreateGameRequest en el body
@router.post("")
async def create_game(request: CreateGameRequest):
    """Endpoint to create a new game."""
    if request.game_name == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    # Crear player (creador de la partida) y partida
    creator = Player(name=request.player_name)
    game = Game(name=request.game_name, creator=creator)

    add_game(game)
    await public_manager.broadcast({"type":"Public_Games","payload": get_listed_games()})
    print(public_manager.connections)
    return CreateGameResponse(game_id=game.unique_id, player_id=creator.unique_id)