from sqlalchemy import create_engine, Column, String, ForeignKey, Table, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .settings import DATABASE_FILENAME

# DB config
engine = create_engine(f'sqlite:///{DATABASE_FILENAME}', echo=False)
Base = declarative_base()

# Association table for the many-to-many relationship
game_player_association = Table('game_player', Base.metadata,
    Column('game_unique_id', String, ForeignKey('Games.unique_id'), primary_key=True),
    Column('player_unique_id', String, ForeignKey('Players.unique_id'), primary_key=True)
)

class Player(Base):
    __tablename__ = 'Players'
    unique_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    games = relationship('Game', secondary=game_player_association, back_populates='players')
    figure_cards = relationship('Figure_card', back_populates='player', cascade="all, delete-orphan")
    movement_cards = relationship('Movement_card', back_populates='player', cascade="all, delete-orphan")
    movements = relationship('Movement', back_populates='player', cascade="all, delete-orphan")

#Player.movements Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or specify a 'primaryjoin' expression.

class Game(Base):
    __tablename__ = 'Games'
    unique_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # "public", "private"
    password = Column(String)
    state = Column(String, nullable=False) # "waiting", "started", "finished"
    # amount of turns that have passed. player[turn%len(players)] is to play
    turn = Column(Integer)
    turn_start_time = Column(DateTime)
    creator = Column(String, ForeignKey('Players.unique_id'))
    players = relationship('Player', secondary=game_player_association, back_populates='games')
    board = Column(String)

class Figure_card(Base):
    __tablename__ = 'Figure_cards'
    unique_id = Column(String, primary_key=True)  # Ensure a primary key exists
    card_type = Column(Integer)
    state = Column(String, nullable=False)  # 'drawn', 'not drawn', 'blocked'
    game_id = Column(String, ForeignKey('Games.unique_id'))
    player_id = Column(String, ForeignKey('Players.unique_id'))

    player = relationship('Player', back_populates='figure_cards')
    game = relationship('Game')

class Movement_card(Base):
    __tablename__ = 'Movement_cards'
    unique_id = Column(String, primary_key=True)  # Ensure a primary key exists
    card_type = Column(Integer)
    state = Column(String)  # 'not blocked', 'blocked'
    
    game_id = Column(String, ForeignKey('Games.unique_id'))
    player_id = Column(String, ForeignKey('Players.unique_id'))

    player = relationship('Player', back_populates='movement_cards')
    game = relationship('Game')

class Movement(Base):
    __tablename__ = 'Movements'
    unique_id = Column(String, primary_key=True)  # Ensure a primary key exists
    from_x = Column(Integer, nullable=False)
    from_y = Column(Integer, nullable=False)
    to_x = Column(Integer, nullable=False)
    to_y = Column(Integer, nullable=False)
    move_number = Column(Integer, nullable=False)
    player_id = Column(String, ForeignKey('Players.unique_id'))
    card_id = Column(String, ForeignKey('Movement_cards.unique_id'))
    # move 0 is the first move that player has made
    player = relationship('Player', back_populates='movements')
    

# Crea las tablas en la base de datos
Base.metadata.create_all(engine)

# Crea una sesión
# Session = sessionmaker(bind=engine)
# session = Session()
# GRACIAS CHUN