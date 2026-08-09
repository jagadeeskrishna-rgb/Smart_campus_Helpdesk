# Smart_campus_Helpdesk
The **Smart Campus Helpdesk Web Application** is a full-stack web-based ticketing system designed to manage and resolve campus-related service requests in an organized and transparent manner. In educational institutions, students frequently face issues such as classroom projector failure, Wi-Fi connectivity problems, lab system errors, hostel maintenance issues, library book requests, lost ID cards, and other administrative service needs. In many cases, these issues are reported manually through phone calls, verbal communication, paper forms, or informal messages, which makes it difficult to track, assign, prioritize, and resolve them efficiently.

This project proposes a centralized digital helpdesk platform inspired by **IT Service Management (ITSM)** principles. The application allows students to register, log in, raise service tickets, upload supporting files or images, track ticket status, and communicate through comments. Admin users can manage service categories, assign tickets to technicians or staff, monitor ticket progress, and view dashboard reports. Technicians can view assigned tickets, update status, add resolution comments, and close issues after completion.

The proposed system improves communication between students and campus support teams, reduces manual tracking work, provides status transparency, and maintains a complete history of ticket activities. The project includes authentication, role-based access control, CRUD operations, file upload, dashboard charts, search/filtering, notifications, ticket workflow, and deployment support. 

This project is developed as an academic web application using Python Django, SQLite, HTML, CSS, JavaScript, and Bootstrap.

## 2. Problem Statement

The main problem addressed by this project is the lack of a centralized and trackable system for handling campus service requests. Students may face many issues inside the campus, but there may not be a proper digital platform to report those issues, track their current status, and confirm whether the issue has been resolved.

In the existing manual process, students may report problems directly to office staff, lab assistants, maintenance staff, or department coordinators. However, these reports may be missed, delayed, duplicated, or not assigned to the correct person. Admin staff may also find it difficult to monitor pending requests, identify high-priority issues, and generate reports.

Therefore, there is a need for a web-based helpdesk system where campus issues can be reported, assigned, tracked, resolved, and analyzed in a structured way.

---

## 3. Existing System / Existing Problem

In many colleges or institutions, service requests are handled using manual or semi-manual methods.

### Existing methods

- Verbal complaint to staff
- Phone call to department or office
- Paper-based complaint register
- WhatsApp or email-based informal communication
- Direct communication with technician or admin staff

### Problems in the existing system

1. **No centralized complaint system**    
Issues are reported through different channels, so tracking becomes difficult.
2. **No proper ticket number**    
Students may not receive a unique reference number for their complaint.
3. **Difficult to track status**    
Students may not know whether the issue is pending, assigned, in progress, or resolved.
4. **Delay in assigning issues**    
Admin staff may take time to identify and assign the issue to the correct technician.
5. **Duplicate complaints**    
The same issue may be reported multiple times without proper grouping or tracking.
6. **No priority management**    
Urgent issues and normal issues may be treated in the same way.
7. **No history or audit trail**    
It is difficult to know who updated the ticket, when it was assigned, and how it was resolved.
8. **No dashboard or report**    
Management cannot easily analyze how many tickets are open, pending, resolved, or category-wise.
9. **Manual communication gap**    
Students, admin staff, and technicians may not have a common communication platform.
10. **Document or image proof not properly stored**    
Supporting files such as issue images, screenshots, or documents may not be stored with the complaint.

---

## 4. Proposed Solution

The proposed solution is a **Smart Campus Helpdesk Web Application** that provides a centralized online platform for campus service request management.

Students can create a ticket by selecting the service category, entering issue details, setting priority, mentioning location, and uploading an attachment if required. Once the ticket is created, the admin can review it and assign it to the appropriate technician or staff member. The technician can update the ticket status as assigned, in progress, resolved, or on hold. Students can track the current status and add comments if additional details are required.

The system maintains a complete ticket history, including status changes, comments, assigned users, and resolution details. Admins can view dashboards with ticket counts, status-wise reports, category-wise reports, and recent tickets. This helps the institution improve service quality, reduce delays, and maintain accountability.

### Advantages of the proposed system

1. Centralized ticket management
2. Unique ticket number for every complaint
3. Role-based access for student, admin, and technician
4. Easy ticket creation and tracking
5. Ticket assignment and status update workflow
6. File/image upload support
7. Comments and communication history
8. Dashboard and report generation
9. Search and filtering options
10. Better transparency and accountability
11. Reduced manual work
12. Improved campus service management

---

## 5. Project Modules

The Smart Campus Helpdesk Web Application contains the following major modules.

---

## 5.1 Authentication Module

The authentication module manages user registration, login, secure password handling, and JWT-based authentication.

### Main features

- Student registration
- User login
- Password encryption

### Users involved

- Student
- Technician / Staff
- Admin

---

## 5.2 Role-Based Access Control Module

This module controls what each user can access based on their role.

### Roles

| Role | Access Details |
| --- | --- |
| Student | Create ticket, view own tickets, upload files, add comments, track status |
| Technician / Staff | View assigned tickets, update status, add resolution comments |
| Admin | Manage users, categories, assign tickets, view all tickets, dashboard and reports |

---

## 5.3 Student Ticket Module

This module allows students to create and manage their service requests.

### Main features

- Create new ticket
- Select service category
- Enter issue title and description
- Select priority
- Enter location
- Upload supporting file/image
- View own tickets
- Track ticket status
- Add comments
- Close/reopen ticket if required

---

## 5.4 Admin Management Module

This module allows the admin to manage the complete helpdesk process.

### Main features

- View all tickets
- Search and filter tickets
- Assign tickets to technician/staff
- Reassign tickets if required
- Manage service categories
- Manage users and roles
- View dashboard reports
- Monitor ticket progress

---

## 5.5 Technician / Staff Module

This module helps technicians manage their assigned service requests.

### Main features

- View assigned tickets
- Check ticket details and attachments
- Change ticket status
- Add work progress comments
- Add resolution notes
- Mark ticket as resolved

---

## 5.6 Service Category Module

This module manages different campus service departments.

### Main categories

1. IT & Network Support
2. Campus Infrastructure & Maintenance
3. Administrative & Student Services
4. Library & Academics

### Example services

| Category | Example Issues |
| --- | --- |
| IT & Network Support | Wi-Fi problem, lab system issue, projector issue, printer problem |
| Campus Infrastructure & Maintenance | Fan/light issue, hostel maintenance, water problem, furniture repair |
| Administrative & Student Services | Lost ID card, bonafide certificate, fee receipt issue, transport pass |
| Library & Academics | Book request, book not available, library card issue, academic document request |

---

## 5.7 Ticket Workflow Module

This module manages the complete lifecycle of a ticket.

### Ticket workflow

```text
New → Assigned → In Progress → Resolved → Closed
```

### Additional statuses

```text
On Hold
Reopened
Rejected
```

### Status meaning

| Status | Description |
| --- | --- |
| New | Ticket created by student and waiting for admin review |
| Assigned | Ticket assigned to technician/staff |
| In Progress | Technician is working on the issue |
| On Hold | Ticket is temporarily paused |
| Resolved | Technician has completed the issue |
| Closed | Issue confirmed and closed |
| Reopened | Student reopened the issue |
| Rejected | Invalid or duplicate ticket rejected by admin |

---

## 5.8 File Upload Module

This module allows users to upload supporting documents or images related to the ticket.

### Main features

- Upload issue image
- Upload document proof
- Store file URL
- Display attachment in ticket details
- Validate file type and size

### Tools used

- Multer for backend upload handling
- Cloudinary for cloud file storage

---

## 5.9 Comments and Ticket History Module

This module maintains communication and audit history for every ticket.

### Main features

- Student comments
- Technician comments
- Admin remarks
- Resolution notes
- Status change history
- Date and time tracking
- User-wise update tracking

---

## 5.10 Notification Module

This module notifies users about important ticket updates.

### Notification examples

- Ticket created successfully
- Ticket assigned to technician
- Ticket moved to in progress
- Ticket resolved
- Ticket reopened
- Ticket closed

---

## 5.11 Dashboard and Reports Module

This module provides visual summary and reports for admin and technician users.

### Dashboard features

- Total tickets
- New tickets
- Assigned tickets
- In-progress tickets
- Resolved tickets
- Closed tickets
- Category-wise tickets
- Priority-wise tickets
- Recent ticket list

### Chart examples

- Ticket status chart
- Category-wise ticket chart
- Priority-wise ticket chart

---

## H/W and S/W Requirements

## 1. Development Requirements

### Hardware Requirements for Development

- Processor: Intel i3 or above
- RAM: Minimum 4 GB, recommended 8 GB
- Hard Disk: Minimum 10 GB free space
- Monitor: Standard monitor
- Keyboard and Mouse
- Internet connection for downloading packages and GitHub usage

### Software Requirements for Development

- Operating System: Windows 10 / Windows 11 / Linux
- Programming Language: Python 3.x
- Framework: Django
- Database: SQLite
- Frontend: HTML, CSS, JavaScript, Bootstrap
- IDE/Editor: Visual Studio Code or PyCharm
- Version Control: Git and GitHub
- Documentation Tool: Confluence
- Task Tracking Tool: Jira
- CI/CD Tool: Jenkins
- Browser: Google Chrome / Microsoft Edge

## 2. Deployment Requirements

### Hardware Requirements for Deployment

For local academic demo:

- Processor: Intel i3 or above
- RAM: Minimum 4 GB
- Storage: Minimum 5 GB free space
- Network: Localhost or LAN access

For future server deployment:

- Processor: 2 Core CPU or above
- RAM: Minimum 2 GB, recommended 4 GB
- Storage: Minimum 20 GB
- Stable internet connection

### Software Requirements for Deployment

For local demo deployment:

- Python 3.x
- Django
- SQLite
- Required Python packages from requirements.txt
- Web browser

For future production deployment:

- Linux server such as Ubuntu or Windows 10 / Windows 11
- Python 3.x
- Django
- Gunicorn or uWSGI
- Nginx web server
- PostgreSQL or MySQL database
- GitHub repository
- Jenkins pipeline for build and testing

