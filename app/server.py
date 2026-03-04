from services.logger_service import registrar_circularizacion
from services.log_reader_service import leer_historial
from services.stats_service import obtener_estadisticas
from fastapi import FastAPI, Request, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.sender_service import procesar_circularizacion
from app.excel_reader import leer_excel
from services.progress_service import obtener_progreso
from services.error_reader_service import leer_errores
from services.retry_service import reintentar_error
from services.stats_service import obtener_estadisticas
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
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
    mensaje: str = Form(...),
    email_remitente: str = Form(...),
    password: str = Form(...)
):

    # guardar Excel
    excel_path = os.path.join(UPLOAD_FOLDER, excel_file.filename)

    with open(excel_path, "wb") as f:
        f.write(await excel_file.read())

    print(f"Excel guardado en: {excel_path}")

    # guardar PDFs
    pdf_paths = []

    for pdf in pdf_files:

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)

        with open(pdf_path, "wb") as f:
            f.write(await pdf.read())

        pdf_paths.append(pdf_path)

        print(f"PDF guardado: {pdf_path}")

    # leer Excel
    destinatarios = leer_excel(excel_path)

    registrar_circularizacion(
        excel_file.filename,
        len(destinatarios),
        email_remitente
    )

    print("DESTINATARIOS DETECTADOS:")
    print(destinatarios)

    # ejecutar envío en segundo plano
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

    return {
        "resultado": resultado
    }

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):

    stats = obtener_estadisticas()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "stats": stats
        }
    )