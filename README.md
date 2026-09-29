# Hospital Management System (Python Flask Version)

This is a full conversion of the PHP Hospital Management System into a modern **Python 3 / Flask** web application featuring **SQLAlchemy ORM**, **Jinja2 Templating**, and multi-role authentication (Patient, Doctor, Admin).

---

## Features

- **Public Landing Page**: Modern carousel header, hospital services, About Us content, interactive Contact Us form submission.
- **Patient Portal (`/patient`)**:
  - Registration & Login
  - Dashboard with summary counters
  - Book Appointment with dynamic AJAX doctor selection by specialization
  - Appointment History with user cancellation
  - View Billing Statements & Invoices
  - Access Lab Blood Reports
  - View Medical History & Prescriptions
  - Profile & Password update
- **Doctor Portal (`/doctor`)**:
  - Doctor Login
  - Dashboard with patient & appointment counts
  - Manage Appointments (Approve/Cancel)
  - Add & Manage Patient Profiles
  - Log Medical History, Vitals (BP, Sugar, Weight, Temp) & Prescriptions
  - Generate & View Lab Blood Test Reports
  - Search Patient Directory by name/phone
  - Profile & Password update
- **Master Admin Portal (`/admin`)**:
  - Admin Login (Default: `admin` / `Test@12345`)
  - Dashboard with system statistics
  - Doctor Specialization Management (Add/Delete)
  - Doctor Management (Add, Edit, Delete)
  - User / Patient Account Management
  - View All Appointments
  - Contact Us Query Management with Admin Remarks
  - Generate, View, Print & Delete Invoices
  - User & Doctor Login Audit Trail Logs
  - Live CMS Page Editing (About Us & Contact Details)

---

## Setup & Running Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
Run the database initialization script to create tables and seed initial data:
```bash
python init_db.py
```

### 3. Start Application
```bash
python app.py
```
Open your browser and navigate to: `http://localhost:5000`

---

## Default Credentials

| Portal | Username / Email | Password |
|---|---|---|
| **Admin** | `admin` | `Test@12345` |
| **Doctor** | `anujk123@test.com` | `Test@123` |
| **Patient** | `johndoe12@test.com` | `Test@123` |
