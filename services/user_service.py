from database.db import SessionLocal
from database.models import Usuario


def obtener_usuarios():

    db = SessionLocal()

    try:

        usuarios_db = db.query(Usuario).all()

        usuarios = {}

        for u in usuarios_db:

            usuarios[u.username] = {
                "email": u.email,
                "role": u.role
            }

        return usuarios

    finally:
        db.close()


def crear_usuario(username, password, email):

    db = SessionLocal()

    try:

        usuario = Usuario(
            username=username,
            password=password,
            email=email,
            role="user"
        )

        db.add(usuario)
        db.commit()

    finally:
        db.close()


def eliminar_usuario(username):

    db = SessionLocal()

    try:

        usuario = db.query(Usuario).filter(
            Usuario.username == username
        ).first()

        if usuario:
            db.delete(usuario)
            db.commit()

    finally:
        db.close()