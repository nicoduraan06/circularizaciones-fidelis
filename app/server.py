from services.logger_service import registrar_circularizacion
from services.log_reader_service import leer_historial
from fastapi import FastAPI, Request, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.sender_service import procesar_circularizacion
from app.excel_reader import leer_excel
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