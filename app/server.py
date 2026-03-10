from services.logger_service import registrar_circularizacion
from services.log_reader_service import leer_historial
from services.stats_service import obtener_estadisticas
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.sender_service import procesar_circularizacion
from app.excel_reader import leer_excel
from services.progress_service import obtener_progreso, iniciar_progreso
from services.error_reader_service import leer_errores
from starlette.middleware.sessions import SessionMiddleware
from services.auth_service import autenticar_usuario
from services.user_service import obtener_usuarios, crear_usuario, eliminar_usuario
from fastapi.staticfiles import StaticFiles
import os

from database.db import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# activar carpeta static para CSS / JS / imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key="clave-super-secreta"
)

templates = Jinja2Templates(directory="templates")

# carpeta temporal compatible con Vercel
UPLOAD_FOLDER = "/tmp/uploads"

# asegurar que existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/login")

    if "smtp_password" not in request.session:
        return RedirectResponse("/configurar_smtp")

    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/historial", response_class=HTMLResponse)
def historial(request: Request, buscar: str = ""):

    registros = leer_historial()

    if buscar:
        buscar_lower = buscar.lower()

        registros = [
            r for r in registros
            if buscar_lower in r["fecha"].lower()
            or buscar_lower in r["excel"].lower()
            or buscar_lower in r["correo"].lower()
        ]

    registros = sorted(registros, key=lambda r: r["fecha"], reverse=True)

    return templates.TemplateResponse(
        "historial.html",
        {
            "request": request,
            "registros": registros,
            "buscar": buscar
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    stats = obtener_estadisticas()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_circularizaciones": stats["total_circularizaciones"],
            "total_destinatarios": stats["total_destinatarios"],
            "ultimos": stats["ultimos"]
        }
    )


@app.get("/configurar_smtp", response_class=HTMLResponse)
def configurar_smtp_page(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/login")

    return templates.TemplateResponse(
        "configurar_smtp.html",
        {"request": request}
    )


@app.post("/configurar_smtp")
async def configurar_smtp(
    request: Request,
    smtp_password: str = Form(...)
):

    request.session["smtp_password"] = smtp_password

    return RedirectResponse("/", status_code=302)


@app.post("/enviar")
async def enviar_circularizacion(
    request: Request,
    excel_file: UploadFile = File(...),
    pdf_files: list[UploadFile] = File(...),
    asunto: str = Form(...),
    mensaje: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse("/login")

    try:

        email_remitente = request.session.get("email")
        password = request.session.get("smtp_password")

        # guardar excel
        excel_filename = os.path.basename(excel_file.filename)
        excel_path = os.path.join(UPLOAD_FOLDER, excel_filename)

        with open(excel_path, "wb") as f:
            f.write(await excel_file.read())

        print(f"Excel guardado en: {excel_path}")

        # guardar PDFs
        pdf_paths = []

        if pdf_files:

            for pdf in pdf_files:

                pdf_filename = os.path.basename(pdf.filename)
                pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

                with open(pdf_path, "wb") as f:
                    f.write(await pdf.read())

                pdf_paths.append(pdf_path)

                print(f"PDF guardado: {pdf_path}")

        # leer excel
        destinatarios = leer_excel(excel_path)

        # iniciar progreso
        iniciar_progreso(len(destinatarios))

        registrar_circularizacion(
            excel_file.filename,
            len(destinatarios),
            email_remitente
        )

        print("DESTINATARIOS DETECTADOS:")
        print(destinatarios)

        procesar_circularizacion(
            destinatarios,
            email_remitente,
            password,
            asunto,
            mensaje
        )

        return templates.TemplateResponse(
            "resultado.html",
            {
                "request": request,
                "total_destinatarios": len(destinatarios)
            }
        )

    except Exception as e:

        print("ERROR EN ENVÍO:")
        print(str(e))

        return HTMLResponse(
            f"Error en la circularización: {str(e)}",
            status_code=500
        )


@app.get("/progreso")
def progreso():
    return obtener_progreso()


@app.get("/errores", response_class=HTMLResponse)
def ver_errores(request: Request):

    errores = leer_errores()

    return templates.TemplateResponse(
        "errores.html",
        {
            "request": request,
            "errores": errores
        }
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/login")

    if request.session.get("role") != "admin":
        return HTMLResponse("Acceso no autorizado", status_code=403)

    stats = obtener_estadisticas()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "stats": stats
        }
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "login_error": False
        }
    )


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    usuario = autenticar_usuario(username, password)

    if not usuario:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "login_error": True
            }
        )

    request.session["user"] = username
    request.session["email"] = usuario["email"]
    request.session["role"] = usuario["role"]

    return RedirectResponse("/configurar_smtp", status_code=302)


@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/login", status_code=302)


@app.get("/usuarios", response_class=HTMLResponse)
def ver_usuarios(request: Request):

    usuarios = obtener_usuarios()

    return templates.TemplateResponse(
        "usuarios.html",
        {
            "request": request,
            "usuarios": usuarios
        }
    )


@app.post("/crear_usuario")
async def crear_usuario_endpoint(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):

    crear_usuario(username, password, email)

    return RedirectResponse("/usuarios", status_code=302)


@app.post("/eliminar_usuario")
async def eliminar_usuario_endpoint(
    username: str = Form(...)
):

    eliminar_usuario(username)

    return RedirectResponse("/usuarios", status_code=302)


@app.post("/analizar_excel")
async def analizar_excel(excel_file: UploadFile = File(...)):

    filename = os.path.basename(excel_file.filename)
    temp_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(temp_path, "wb") as f:
        f.write(await excel_file.read())

    try:

        destinatarios = leer_excel(temp_path)

        return {
            "total_destinatarios": len(destinatarios)
        }

    except Exception as e:

        return {
            "error": str(e)
        }