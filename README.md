# Circularizaciones Fidelis

Automated circularization system for sending large volumes of emails with PDF attachments based on Excel input.

This internal tool was developed to automate the circularization process used in audit workflows, allowing employees to upload an Excel file with recipients and automatically send personalized emails with the corresponding PDF attachments.

The system is designed to handle large batches of emails efficiently while providing real-time progress tracking, error management, and delivery reporting.

---

## Overview

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

## Main Features

### Excel-driven email sending

- Reads recipient data from Excel
- Supports flexible column formats and header detection
- Allows **multiple recipients per row**
- Automatically matches documents with their corresponding PDF

### Automated PDF matching

The system automatically finds the correct PDF file even if:

- Filenames contain spaces
- Filenames contain accents or special characters
- Filenames contain URL-encoded characters

Filenames are normalized to ensure reliable attachment matching regardless of formatting.

### Direct file upload

PDFs are uploaded directly to the server and stored temporarily in `/tmp` during processing.

- No external storage dependencies
- No operation limits
- Simpler and faster workflow

### Parallel email sending

Emails are sent using **ThreadPoolExecutor**, allowing parallel processing.

- Faster circularizations
- Reduced total sending time
- Improved reliability for large batches

### Real-time progress tracking

Users can monitor circularization progress directly from the interface.

The system displays:

- Number of emails processed
- Number of successful deliveries
- Number of errors

### Delivery evidence report

After each circularization the sender automatically receives a summary email containing:

- Successfully delivered emails
- Failed emails
- Total recipients processed

This provides **delivery evidence for audit purposes**.

### Error tracking system

All delivery errors are recorded in the system.

Users can review:

- Failed emails
- Error messages
- Full delivery history

### User authentication and roles

The application includes a login system with role-based access control.

| Role | Permissions |
|------|-------------|
| Admin | Full access including user management |
| User | Send circularizations, view history and errors |

---

## Architecture

| Layer | Technology |
|-------|------------|
| Frontend | HTML / CSS / JavaScript |
| Backend | FastAPI (Python) |
| Email sending | SMTP (Gmail) |
| File storage | `/tmp` (serverless temporary storage) |
| Database | Neon PostgreSQL |
| ORM | SQLAlchemy |
| Deployment | Vercel Serverless |

---

## Email Sending Workflow

```
1. User logs in
2. User uploads Excel file and PDF documents
3. Excel file is parsed and recipients are extracted
4. Each recipient is matched with the corresponding PDF
5. Emails are sent in parallel via SMTP
6. Progress is displayed in real time
7. Sender receives a delivery summary report
```

---

## Database Schema

### usuarios
Stores application users.

| Field | Type |
|-------|------|
| id | Integer (PK) |
| username | String |
| password | String |
| email | String |
| role | String |

### circularizaciones
Stores circularization history.

| Field | Type |
|-------|------|
| id | Integer (PK) |
| fecha | DateTime |
| excel | String |
| correo | String |
| destinatarios | Integer |

### errores_envio
Stores email delivery errors.

| Field | Type |
|-------|------|
| id | Integer (PK) |
| fecha | DateTime |
| destinatario | String |
| error | String |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (Neon) |

> SMTP credentials are entered by the user at login and stored only for the duration of the session.

---

## Deployment

The application is deployed using **Vercel Serverless Functions**.

Adaptations implemented for the serverless environment:

- Temporary files stored in `/tmp`
- Compatibility with read-only filesystem
- Asynchronous background tasks for email sending

---

## Project Structure

```
circularizaciones-fidelis/

api/
    index.py                  # Vercel serverless entry point

app/
    excel_reader.py           # Excel parsing and recipient extraction
    mailer.py                 # SMTP email sending
    server.py                 # FastAPI routes and application logic

config/
    users.json                # Legacy user config (replaced by database)

database/
    db.py                     # SQLAlchemy engine and session
    models.py                 # Database models and initial admin setup

services/
    auth_service.py           # User authentication
    error_logger_service.py   # Error logging to CSV
    error_reader_service.py   # Error reading from CSV
    log_reader_service.py     # Circularization history reading
    logger_service.py         # Circularization history writing
    progress_service.py       # Real-time progress tracking
    sender_service.py         # Email sending orchestration
    stats_service.py          # Statistics calculation
    user_service.py           # User management

templates/
    admin.html                # Admin panel
    base.html                 # Base layout
    configurar_smtp.html      # SMTP configuration
    dashboard.html            # Statistics dashboard
    errores.html              # Error tracking
    form.html                 # New circularization form
    historial.html            # Circularization history
    login.html                # Login page
    resultado.html            # Progress and result page
    usuarios.html             # User management

static/
    css/
        style.css             # Global styles
    images/
        logo-fidelis.png      # Company logo
        iconito_fidelis.png   # Favicon

main.py                       # PyCharm entry point (not used in production)
requirements.txt              # Python dependencies
package.json                  # Node dependencies
vercel.json                   # Vercel deployment configuration
.gitignore
```

---

## Reliability Improvements

Several mechanisms ensure stable circularizations:

- Filename normalization for robust PDF matching
- Parallel email sending with ThreadPoolExecutor
- SQLAlchemy connection health checks (`pool_pre_ping`)
- Automatic connection recycling (`pool_recycle`)
- Delivery summary report sent to the sender after each circularization

---

## Future Improvements

- Automatic retry system for failed emails
- PDF preview before sending
- Advanced analytics dashboard
- Email template editor
- Exportable audit reports
- Circularization scheduling

---

## Author

Developed by **Nicolás Durán**

This project was created to automate internal circularization processes and improve efficiency in audit-related workflows at **Grupo Fidelis**.