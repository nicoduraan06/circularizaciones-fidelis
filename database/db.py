import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # verifica si la conexión sigue viva
    pool_recycle=300      # recicla conexiones cada 5 minutos
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)