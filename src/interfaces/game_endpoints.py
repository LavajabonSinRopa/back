# back/interfaces/game_endpoints.py

from fastapi import APIRouter, HTTPException, Response
from entities.game.game_utils import (add_game, get_games, get_game_by_id, 
                                      add_to_game, remove_player_from_game, pass_turn,
                                      start_game_by_id,get_game_status,is_players_turn,make_temp_movement,
                                      remove_top_movement, apply_temp_movements, complete_figure, FigureResult, block_figure)

from entities.player.player_utils import add_player
from schemas.game_schemas import (CreateGameRequest, CreateGameResponse, 
                                  SkipTurnRequest, JoinGameRequest, JoinGameResponse,
                                  LeaveGameRequest, MakeMoveRequest, UnmakeMoveRequest,
                                  applyTempMovementsRequest, CompleteFigureRequest, BlockFigureRequest)
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
    game_id = add_game(game_name=request.game_name, creator_id=creator_id, password=request.password)
    
    game_socket_manager.create_game_map(game_id)
    game_socket_manager.join_player_to_game_map(game_id,creator_id)
    
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
    try:
        add_to_game(player_id=player_id, game_id=game_id, password=request.password)
    except:
        raise HTTPException(status_code=403, detail="Invalid password")
    game_socket_manager.join_player_to_game_map(game_id,player_id)

    # Avisar a los sockets de la partida sobre el jugador que se une.
    await game_socket_manager.broadcast_game(game_id,{"type":"PlayerJoined","payload": {'player_id' : player_id, 'player_name': request.player_name}})
    
    #Actualizar la cantidad de jugadores a los que buscan partida.
    await public_manager.broadcast({"type":"CreatedGames","payload": get_games()})

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
    if game["creator"] == request.player_id and game["state"] == "waiting":
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

    # Avisar a los sockets de la partida de un potencial cambio en el tablero (si el jugador que abandona tenía movimientos parciales hechos)
    if(game["state"]!="waiting"):
        await game_socket_manager.broadcast_game(game_id,{"type":"MoveUnMade","payload": get_game_status(game_id)})
    
    game["player_names"].remove(player_name)
    game['players'].remove(request.player_id)
    if len(game['players']) <= 1:
        await game_socket_manager.broadcast_game(game_id,{"type":"GameWon","payload": {'player_id' : game['players'][0], 'player_name': game['player_names'][0]}})
        
    #Actualizar la cantidad de jugadores a los que buscan partida.
    if(game['state']=='waiting'):
        await public_manager.broadcast({"type":"CreatedGames","payload": get_games()})

    # Devolver 200 OK sin data extra
    return Response(status_code=200)

@router.post("/{game_id}/cancel")
async def cancel_game(game_id: str, request: LeaveGameRequest):
    """Endpoint to cancel a game."""
    try:
        game = get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")
    
    # Verificar que el juego está en estado "waiting"
    if(game['state']!='waiting'):
        raise HTTPException(status_code=403, detail="No se puede eliminar un juego que ya comenzó o terminó")

    # Verificar que el jugador sea el creador del juego
    if game["creator"] != request.player_id:
        raise HTTPException(status_code=403, detail="Sólo puede cancelar la partida el creador del juego")
    
    # Avisar a los jugadores que se cancela la partida
    await game_socket_manager.broadcast_game(game_id,{"type":"GameClosed","payload": "Game Closed, disconnected"})
    
    return Response(status_code=200)


@router.post("/{game_id}/skip")
async def skip_turn(game_id: str, request: SkipTurnRequest):
    """Endpoint to join a game."""
    try:
        skipped = pass_turn(game_id=game_id,player_id=request.player_id)
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")

    if(skipped):
        # Avisar a los demás jugadores del nuevo estado de la partida
        await game_socket_manager.broadcast_game(game_id,{"type":"TurnSkipped","payload": get_game_status(game_id=game_id)})
        return Response(status_code=200)

    #Si no pudo saltear
    else:
        raise HTTPException(status_code=418, detail="Not your turn")
    
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
    try:
        start_game_by_id(game_id)
    except ValueError:
        raise HTTPException(status_code=403, detail="La partida ya está iniciada")
    
    # Avisar a los sockets de la partida sobre el comienzo de la partida.
    await game_socket_manager.broadcast_game(game_id,{"type":"GameStarted","payload": get_game_status(game_id)})

    # Devolver 200 OK sin data extra
    return Response(status_code=200)


@router.post("/{game_id}/move")
async def make_move(game_id: str,request: MakeMoveRequest):
    #fijarse si existe la partida y es el turno del jugador
    try: 
        if(not is_players_turn(player_id=request.player_id, game_id=game_id)):
            raise HTTPException(status_code=403, detail="No es tu turno")
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")

    #intentar hacer el movimiento
    try:
        moved = make_temp_movement(game_id=game_id,player_id=request.player_id, card_id=request.card_id, from_x=request.from_x, from_y=request.from_y, to_x=request.to_x, to_y=request.to_y)
        if(not moved):
            raise HTTPException(status_code=403, detail="Invalid Move")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An exception occurred")
    
    # Avisar a los sockets de la partida sobre el movimiento hecho
    await game_socket_manager.broadcast_game(game_id,{"type":"MovSuccess","payload": get_game_status(game_id)})

    return Response(status_code=200)

@router.post("/{game_id}/unmove")
async def unmake_move(game_id: str,request: UnmakeMoveRequest):
    #fijarse si existe la partida y es el turno del jugador
    try: 
        if(not is_players_turn(player_id=request.player_id, game_id=game_id)):
            raise HTTPException(status_code=403, detail="No es tu turno")
    except:
        raise HTTPException(status_code=404, detail="Invalid game ID")

    try:
        remove_top_movement(game_id=game_id,player_id=request.player_id)
        await game_socket_manager.broadcast_game(game_id,{"type":"MoveUnMade","payload": get_game_status(game_id)})
    except:
        raise HTTPException(status_code=403, detail="Invalid Move")
    return Response(status_code=200)

@router.post("/{game_id}/apply")
async def apply_moves(game_id: str,request: applyTempMovementsRequest):
    try:
        if(not is_players_turn(player_id=request.player_id, game_id=game_id)):
            raise HTTPException(status_code=403, detail="No es tu turno")
        apply_temp_movements(game_id=game_id,player_id=request.player_id)
        await game_socket_manager.broadcast_game(game_id,{"type":"MovesApplied","payload": get_game_status(game_id)})
    except:
        raise HTTPException(status_code=403, detail="Invalid Move")
    return Response(status_code=200)
        
@router.post("/{game_id}/completeFigure")
async def complete_own_figure(game_id: str, request: CompleteFigureRequest):
    try:
        result = complete_figure(game_id=game_id, player_id=request.player_id, card_id=request.card_id, i = request.y, j = request.x)
        
        if result == FigureResult.PLAYER_WON:
            game = get_game_by_id(game_id)
            winner_index = game["players"].index(request.player_id)
            winner_name = game["player_names"][winner_index]
            await game_socket_manager.broadcast_game(game_id,{"type":"GameWon","payload": {'player_id' : request.player_id, 'player_name': winner_name}})
        else:  # FigureResult.COMPLETED
            await game_socket_manager.broadcast_game(game_id,{"type":"FigureMade","payload": get_game_status(game_id)})
        
        return Response(status_code=200)
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Invalid Figure")
    
    return Response(status_code=200)

@router.post("/{game_id}/blockFigure")
async def complete_own_figure(game_id: str,request: BlockFigureRequest):
    try:
        block_figure(game_id=game_id, player_id=request.player_id, card_id=request.card_id, i = request.y, j = request.x)
        await game_socket_manager.broadcast_game(game_id,{"type":"FigureBlocked","payload": get_game_status(game_id)})
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Invalid Figure")
    
    return Response(status_code=200)
