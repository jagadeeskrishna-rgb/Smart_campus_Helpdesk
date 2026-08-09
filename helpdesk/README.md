# Smart Campus Helpdesk Web Application

    A complete academic Django web application for campus service-request management. The system supports student ticket creation, administrator assignment and monitoring, technician status updates, comments, validated file uploads, ticket history, notifications, and dashboard reports.

    ## Technology

    - Backend: Django 5.2
    - Frontend: HTML, CSS, JavaScript, Bootstrap 5, Chart.js
    - Database: SQLite for academic demo, PostgreSQL-ready for production
    - Testing: Django TestCase
    - Deployment: Local demo with future Gunicorn, Nginx, PostgreSQL, and Jenkins pipeline

    ## Quick Start

    ```powershell
    cd source_code
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    copy .env.example .env
    python manage.py migrate
    python manage.py seed_demo
    python manage.py runserver
    ```

    Demo users after seeding:

    - Admin: `admin` / `Admin@12345`
    - Technician: `technician` / `Tech@12345`
    - Student: `student` / `Student@12345`

    ## Modules

    | Module | Purpose |
| --- | --- |
| Authentication Module | Registration, login, logout, profile roles, and secure password handling. |
| Role-Based Access Control Module | Server-side permissions for Student, Technician, and Admin workflows. |
| Student Ticket Module | Ticket creation, tracking, comments, close, and reopen actions. |
| Admin Management Module | Ticket assignment, category management, search, filters, dashboards, and reports. |
| Technician Staff Module | Assigned-ticket queue, work updates, status changes, and resolution notes. |
| Service Category Module | Campus department and service category maintenance. |
| Ticket Workflow Module | Controlled transitions from New through Assigned, In Progress, Resolved, Closed, and Reopened. |
| File Upload Module | Validated image/document uploads stored through Django media storage. |
| Comments and Ticket History Module | Ticket discussion, status history, audit trail, and resolution records. |
| Notification Module | In-app notifications for important ticket lifecycle events. |
| Dashboard and Reports Module | Role-aware counters, charts, recent ticket lists, and report filters. |

    ## Important Folders

    - `source_code/`: runnable Django application.
    - `documentation/`: academic report, setup, deployment, troubleshooting, project guide, and test report.
    - `diagrams/`: editable Mermaid sources and exported SVG diagrams.
    - `tests/`: test-case catalogue and validation notes.
    - `deployment/`: production-oriented deployment samples.
