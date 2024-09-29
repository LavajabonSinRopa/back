from sqlalchemy import create_engine, Column, String, ForeignKey, Table, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .settings import DATABASE_FILENAME

# DB config
engine = create_engine(f'sqlite:///{DATABASE_FILENAME}', echo=True)
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

class Game(Base):
    __tablename__ = 'Games'
    unique_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    board = Column(String)
    creator = Column(String, ForeignKey('Players.unique_id'))
    players = relationship('Player', secondary=game_player_association, back_populates='games')

class Figure_card(Base):
    __tablename__ = 'Figure_cards'
    card_type = Column(Integer)
    # 'Drawn' 'Not drawn' 'Blocked'
    state = Column(String, nullable=False)
    player = relationship('Player', back_populates='figure_cards')
    pass

class Movement_card(Base):
    __tablename__ = 'Movement_cards'
    card_type = Column(Integer)
    player = relationship('Player', back_populates='Movement_cards')
    pass

# Crea las tablas en la base de datos
Base.metadata.create_all(engine)

# Crea una sesión
# Session = sessionmaker(bind=engine)
# session = Session()
# GRACIAS CHUN