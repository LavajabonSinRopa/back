from sqlalchemy import create_engine, Column, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .settings import DATABASE_FILENAME

# Configuración de la base de datos
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

class Game(Base):
    __tablename__ = 'Games'
    unique_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    board = Column(String)
    creator = Column(String, ForeignKey('Players.unique_id'))
    players = relationship('Player', secondary=game_player_association, back_populates='games')

# Crea las tablas en la base de datos
Base.metadata.create_all(engine)

# Crea una sesión
# Session = sessionmaker(bind=engine)
# session = Session()
# GRACIAS CHUN