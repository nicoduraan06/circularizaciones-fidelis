from services.logger_service import registrar_circularizacion
from services.log_reader_service import leer_historial
from services.stats_service import obtener_estadisticas
from fastapi import FastAPI, Request, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.sender_service import procesar_circularizacion
from app.excel_reader import leer_excel
from services.progress_service import obtener_progreso
from services.error_reader_service import leer_errores
from services.retry_service import reintentar_error
from starlette.middleware.sessions import SessionMiddleware
from services.auth_service import autenticar_usuario
from services.user_service import obtener_usuarios, crear_usuario, eliminar_usuario
import os

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="clave-super-secreta"
)

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"

# contraseña SMTP del sistema (la que ya usabas)
SMTP_PASSWORD = "pdozlfkifknatdxb"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/login")

    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/historial", response_class=HTMLResponse)
def historial(request: Request):

    registros = leer_historial()

    return templates.TemplateResponse(
        "historial.html",
        {
            "request": request,
            "registros": registros
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


@app.post("/enviar")
async def enviar_circularizacion(
    request: Request,
    background_tasks: BackgroundTasks,
    excel_file: UploadFile = File(...),
    pdf_files: list[UploadFile] = File(...),
    asunto: str = Form(...),
    mensaje: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse("/login")

    email_remitente = request.session.get("email")
    password = SMTP_PASSWORD

    excel_path = os.path.join(UPLOAD_FOLDER, excel_file.filename)

    with open(excel_path, "wb") as f:
        f.write(await excel_file.read())

    print(f"Excel guardado en: {excel_path}")

    pdf_paths = []

    for pdf in pdf_files:

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)

        with open(pdf_path, "wb") as f:
            f.write(await pdf.read())

        pdf_paths.append(pdf_path)

        print(f"PDF guardado: {pdf_path}")

    destinatarios = leer_excel(excel_path)

    registrar_circularizacion(
        excel_file.filename,
        len(destinatarios),
        email_remitente
    )

    print("DESTINATARIOS DETECTADOS:")
    print(destinatarios)

    background_tasks.add_task(
        procesar_circularizacion,
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


@app.post("/reintentar")
async def reintentar_envio(
    destinatario: str = Form(...),
    email_remitente: str = Form(...),
    password: str = Form(...),
    asunto: str = Form(...),
    mensaje: str = Form(...)
):

    resultado = reintentar_error(
        email_remitente,
        password,
        destinatario,
        asunto,
        mensaje
    )

    return {"resultado": resultado}


@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/login")

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
        {"request": request}
    )


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    usuario = autenticar_usuario(username, password)

    if not usuario:
        return {"error": "Credenciales incorrectas"}

    request.session["user"] = username
    request.session["email"] = usuario["email"]

    return RedirectResponse("/", status_code=302)

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