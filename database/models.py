from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from database.db import SessionLocal

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


def crear_admin_inicial():

    db = SessionLocal()

    try:

        admins = [
            {
                "username": "Angela Vizcaino",
                "password": "grupofidelis",
                "email": "avizcaino@grupofidelis.es",
                "role": "admin"
            },
            {
                "username": "Nicolas Duran",
                "password": "grupofidelis",
                "email": "nicolasdu2006@gmail.com",
                "role": "admin"
            }
        ]

        for admin_data in admins:

            existe_admin = db.query(Usuario).filter(
                Usuario.username == admin_data["username"]
            ).first()

            if not existe_admin:

                admin = Usuario(**admin_data)

                db.add(admin)

        db.commit()

        print("ADMINS INICIALES VERIFICADOS")

    finally:
        db.close()