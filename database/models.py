from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    role = Column(String)


class Circularizacion(Base):
    __tablename__ = "circularizaciones"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    excel = Column(String)
    correo = Column(String)
    destinatarios = Column(Integer)


class ErrorEnvio(Base):
    __tablename__ = "errores_envio"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    destinatario = Column(String)
    error = Column(String)