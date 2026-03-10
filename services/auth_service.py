from database.db import SessionLocal
from database.models import Usuario


def autenticar_usuario(username, password):

    db = SessionLocal()

    try:

        usuario = db.query(Usuario).filter(
            Usuario.username == username
        ).first()

        if usuario and usuario.password == password:

            return {
                "email": usuario.email,
                "role": usuario.role
            }

        return None

    finally:
        db.close()