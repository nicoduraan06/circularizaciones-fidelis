# Circularizaciones Fidelis

Automated circularization system for sending large volumes of emails with PDF attachments based on Excel input.

This internal tool was developed to automate the circularization process used in audit workflows, allowing employees to upload an Excel file with recipients and automatically send personalized emails with the corresponding PDF attachments.

The system is designed to handle large batches of emails efficiently while providing real-time progress tracking, error management, and delivery reporting.

---

# Overview

Circularizaciones Fidelis is a web application built with **FastAPI** that automates the process of sending circularization emails.

Users upload:

- An **Excel file** containing recipient information
- The **PDF documents** referenced in the Excel

The system then:

1. Parses the Excel file
2. Matches each row with the corresponding PDF
3. Sends emails in parallel using SMTP
4. Tracks progress in real time
5. Stores circularization history in a PostgreSQL database
6. Sends a **delivery report to the sender**

---

# Main Features

## Excel-driven email sending

- Reads recipient data from Excel
- Supports flexible column formats
- Allows **multiple recipients per row**
- Automatically matches documents with their corresponding PDF

---

## Automated PDF matching

The system automatically finds the correct PDF file even if:

- filenames contain spaces
- filenames contain accents
- filenames contain URL encoding characters

The system normalizes filenames to ensure reliable attachment matching.

---

## Direct file upload

PDFs are uploaded directly to the server and stored temporarily in `/tmp` during processing.

Benefits:

- no external storage dependencies
- no operation limits
- simpler and faster workflow

---

## Parallel email sending

Emails are sent using **ThreadPoolExecutor**, allowing parallel processing.

Benefits:

- faster circularizations
- reduced total sending time
- improved reliability

---

## Real-time progress tracking

Users can monitor circularization progress directly from the interface.

The system shows:

- number of processed emails
- number of successful deliveries
- number of errors

---

## Delivery evidence report

After each circularization the sender automatically receives a summary email containing:

- successfully delivered emails
- failed emails
- total recipients processed

This provides **delivery evidence for audit purposes**.

---

## Error tracking system

All delivery errors are recorded in the system.

Users can review:

- failed emails
- error messages
- delivery history

---

## User authentication and roles

The application includes a login system with role-based access.

Roles:

- **Admin**
- **User**

Admins can manage users and access administrative panels.

---

# Architecture

The system is built using the following stack:

Frontend  
HTML / CSS / JavaScript

Backend  
FastAPI (Python)

Email sending  
SMTP (Gmail)

File storage  
/tmp (serverless temporary storage)

Database  
Neon PostgreSQL

ORM  
SQLAlchemy

Deployment  
Vercel Serverless

---

# Email Sending Workflow

1. User logs in
2. User uploads Excel file
3. User uploads PDF documents
4. Excel file is parsed
5. Each row is matched with the corresponding PDF
6. Emails are sent in parallel
7. Progress is displayed in real time
8. Sender receives a delivery summary report

---

# Database Schema

## usuarios

Stores application users.

Fields:

- id
- username
- password
- email
- role

---

## circularizaciones

Stores circularization history.

Fields:

- id
- fecha
- excel
- correo
- destinatarios

---

## errores_envio

Stores email delivery errors.

Fields:

- id
- fecha
- destinatario
- error

---

# Environment Variables

The application requires the following environment variables:

```
DATABASE_URL
```

SMTP credentials are provided by the user during login.

---

# Deployment

The application is deployed using **Vercel serverless functions**.

Special adaptations were implemented to support the serverless environment:

- temporary files stored in `/tmp`
- compatibility with read-only filesystem
- asynchronous background tasks

---

# Project Structure

```
circularizaciones-fidelis/

api/
    blob-upload.js
    index.py

app/
    excel_reader.py
    mailer.py
    server.py

config/
    users.json

database/
    db.py
    models.py

services/
    auth_service.py
    error_logger_service.py
    error_reader_service.py
    log_reader_service.py
    logger_service.py
    progress_service.py
    sender_service.py
    stats_service.py
    user_service.py

templates/
    admin.html
    base.html
    configurar_smtp.html
    dashboard.html
    errores.html
    form.html
    historial.html
    login.html
    resultado.html
    usuarios.html

static/
    css/
        style.css
    images/
        logo-fidelis.png

logs/
    circularizaciones.log
    errores_envio.csv

main.py
requirements.txt
package.json
vercel.json
.gitignore
```

---

# Reliability Improvements

Several mechanisms ensure stable circularizations:

- filename normalization for PDF matching
- parallel email sending
- SQLAlchemy connection health checks
- delivery summary reporting

---

# Future Improvements

Possible future enhancements include:

- automatic retry system for failed emails
- PDF preview before sending
- advanced analytics dashboard
- email template editor
- exportable audit reports
- circularization scheduling

---

# Author

Developed by **Nicolás Durán**

This project was created to automate internal circularization processes and improve efficiency in audit-related workflows.