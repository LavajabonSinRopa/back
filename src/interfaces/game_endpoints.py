# back/interfaces/game_endpoints.py

from fastapi import APIRouter, HTTPException
from entities.game.game_utils import add_game, get_games, get_game_by_id, add_to_game
from entities.player.player_utils import add_player
from schemas.game_schemas import (CreateGameRequest, CreateGameResponse, 
                                  GameInResponse, JoinGameRequest, JoinGameResponse)
from interfaces.SocketManagers import public_manager, game_socket_manager 

router = APIRouter()

# POST a /games -- Crear partida. recibe JSON de tipo CreateGameRequest en el body
@router.post("")
async def create_game(request: CreateGameRequest):
    """Endpoint to create a new game."""
    if request.game_name == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    # Crear player (creador de la partida) y partida
    creator_id = add_player(player_name=request.player_name)
    game_id = add_game(game_name=request.game_name, creator_id=creator_id)
    
    game_socket_manager.create_game_map(game_id)
    game_socket_manager.join_player_to_game_map(game_id,creator_id)
    
    #TODO: send only data of games in "waiting"
    await public_manager.broadcast({"type":"CreatedGames","payload": get_games()})
    
    return CreateGameResponse(game_id=game_id, player_id=creator_id)

@router.post("/{game_id}/join", response_model=JoinGameResponse)
async def join_game(game_id: str, request: JoinGameRequest):
    """Endpoint to join a game."""
    try:
        game = get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")
    
    # Crear player, agregarlo al juego
    player_id = add_player(player_name=request.player_name)
    add_to_game(player_id=player_id, game_id=game_id)
    game_socket_manager.join_player_to_game_map(game_id,player_id)

    #Avisar a los sockets de la partida sobre la union.
    await game_socket_manager.broadcast_game(game_id,{"type":"PlayerJoined","payload": request.player_name})

    # Devolver ID unico de jugador para la partida
    return JoinGameResponse(player_id=player_id)

@router.get("")
def get_all_games():
    """Endpoint to request all games"""
    games = get_games()
    return games