# back/entities/game.py

import uuid
from ..player.player import Player

class Game:
    def __init__(self, name: str, creator: Player):
        self.name = name
        self.unique_id = str(uuid.uuid4())
        self.creator = creator
        self.players = [creator]  # Lista de jugadores con creator añadido autom.
        self.state = "waiting"    # Estado del juego: waiting, started, ended
        self.board = None         