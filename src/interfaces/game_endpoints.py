# back/interfaces/game_endpoints.py

from fastapi import APIRouter, HTTPException, Response
from entities.game.game_utils import (add_game, get_games, get_game_by_id, 
                                      add_to_game, remove_player_from_game, pass_turn,
                                      start_game_by_id,get_players_status)
from entities.player.player_utils import add_player
from schemas.game_schemas import (CreateGameRequest, CreateGameResponse, 
                                  SkipTurnRequest, JoinGameRequest, JoinGameResponse,
                                  LeaveGameRequest)
from interfaces.SocketManagers import public_manager, game_socket_manager 
from sqlalchemy.exc import NoResultFound

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
    
    if game["state"] != "waiting":
        raise HTTPException(status_code=403, detail="La partida no está en estado de espera")
    
    # Validar cantidad de jugadores
    if(len(game["players"]) >= 4):
        raise HTTPException(status_code=403, detail="Game is full!")

    # Crear player, agregarlo al juego
    player_id = add_player(player_name=request.player_name)
    add_to_game(player_id=player_id, game_id=game_id)
    game_socket_manager.join_player_to_game_map(game_id,player_id)
    
    # Avisar a los sockets de la partida sobre el jugador que abandona.
    await game_socket_manager.broadcast_game(game_id,{"type":"PlayerJoined","payload": {'player_id' : player_id, 'player_name': request.player_name}})

    # Devolver ID unico de jugador para la partida
    return JoinGameResponse(player_id=player_id)

@router.post("/{game_id}/leave")
async def leave_game(game_id: str, request: LeaveGameRequest):
    """Endpoint to join a game."""
    try:
        game = get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")
    
    # Verificar si el jugador es el creador del juego
    if game["creator"] == request.player_id:
        raise HTTPException(status_code=403, detail="El creador del juego no puede abandonar la partida")
    
    # Eliminar jugador
    try:
        remove_player_from_game(game_id=game_id, player_id=request.player_id)
    except:
        raise HTTPException(status_code=404, detail="Player does not exist in the game")
    
    # Get name of the player
    player_name = game['player_names'][game['players'].index(request.player_id)]
    
    # Avisar a los sockets de la partida sobre el jugador que abandona.
    await game_socket_manager.broadcast_game(game_id,{"type":"PlayerLeft","payload": {'player_id' : request.player_id, 'player_name': player_name}})

    # Devolver 200 OK sin data extra
    return Response(status_code=200)

@router.post("/{game_id}/skip")
async def skip_turn(game_id: str, request: SkipTurnRequest):
    """Endpoint to join a game."""
    try:
        skipped = pass_turn(game_id=game_id,player_id=request.player_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")

    if(skipped):
        # Devolver 200 OK sin data extra
        return Response(status_code=200)
    
    #Si no pudo saltear
    else:
        raise HTTPException(status_code=418, detail="Not your turn")
    
    #TODO: avisar a los otros juagdores que el turno fue salteado
    
@router.get("")
def get_all_games():
    """Endpoint to request all games"""
    games = get_games()
    return games

@router.get("/{game_id}")
async def get_game(game_id: str):
    """Get data for a specific game."""
    try:
        game = get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")
    
    return game

@router.post("/{game_id}/start")
async def start_game(game_id: str, request: LeaveGameRequest):
    """Endpoint to start a game."""
    try:
        game = get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")
    
    # Verificar si el jugador es el creador del juego
    if game["creator"] != request.player_id:
        raise HTTPException(status_code=403, detail="Solo el creador puede iniciar la partida")
    
    # Iniciar Partida
    start_game_by_id(game_id)
    
    # Avisar a los sockets de la partida sobre el comienzo de la partida.
    await game_socket_manager.broadcast_game(game_id,{"type":"GameStarted","payload": get_players_status(game_id)})

    # Devolver 200 OK sin data extra
    return Response(status_code=200)