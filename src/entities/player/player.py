# back/entities/player.py

import uuid

class Player:
    def __init__(self, name: str, is_owner: bool = False):
        self.unique_id = str(uuid.uuid4())
        self.name = name
        self.figure_deck = []  # Cartas figura
        self.movement_deck = [] # Cartas movimiento
        
        ## ESTO ES MUY TEMPORAL HASTA QUE TENGAMOS BASE DE DATOS
        from interfaces.websocket_interface import playersSockets 
        playersSockets[self.unique_id] = None
