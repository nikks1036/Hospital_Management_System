
# Hospital Management System (HMS)

The **Hospital Management System (HMS)** is a full-featured, enterprise-grade web application engineered to streamline hospital operations, automate patient care workflows, manage doctor schedules, and deliver automated diagnostic lab report management.

Designed with a modern role-based architecture, HMS bridges the communication gap between patients, healthcare providers, and administrative personnel while enforcing strict clinical precision, standardized diagnostic reporting, digital report verification, and automated notification channels.
---

## Visual Interface & Portal Previews

### 1. Landing Page & Public Services
The public interface welcomes visitors with a modern hero slider, hospital services showcase, department overview, and a direct online appointment booking module.

![Dashboard]("Dashboard.png.png")

---

### 2. Multi-Portal Access Selection
Patients, medical practitioners, and system administrators can seamlessly authenticate into their respective specialized portals from a unified access gateway.

![Panal]("panal.png.png")

---

### 3. Administrator Dashboard & Management Console
The centralized admin dashboard provides real-time statistics, active counter cards, user governance controls, medical appointment logs, and pathology lab report builders.

![Admin Panal]("Admin_panal.png.png")

---

## Core System Modules & Features

### 👤 Patient Portal
* **Account Registration & Authentication**: Secure registration with auto-salutation formatting, profile management, and contact updates.
* **Online Appointment Booking**: Select medical specialization, doctor availability, preferred date/time slots, and track booking status.
* **Appointment History & Status Tracking**: Real-time visibility into active, completed, or canceled clinical visits.
* **Prescriptions & Medical Records**: Access digital prescriptions written by consulting physicians.
* **Lab Reports & Diagnostic Center**: View, download, and print standardized single and multi-test pathology lab reports.
* **One-Click WhatsApp Sharing**: Share authentic diagnostic reports instantly with family or specialists via encrypted WhatsApp API integration.
* **Secure Document Wallet**: Store and manage patient-uploaded medical records securely.

---

### 👨‍⚕️ Doctor Portal
* **Practitioner Dashboard**: Overview of upcoming daily consultations, pending appointments, and patient statistics.
* **Patient Management**: Inspect patient medical history, previous diagnoses, and clinical visit history.
* **Appointment Handling**: Approve, re-schedule, or update appointment outcomes.
* **Digital Prescription Builder**: Issue structured prescriptions containing medication details, dosage instructions, and clinical advice.
* **Session Logs & Audit Trails**: Review session logs for login security compliance.

---

### 🛡️ Administrator Portal
* **Executive Dashboard**: High-level statistical overview monitoring total patients, registered doctors, appointment volumes, and public inquiries.
* **Doctor Governance**: Add, edit, or deactivate doctor profiles, assign specializations, manage consultation fees, and set working schedules.
* **User & Patient Management**: Comprehensive patient record control, contact management, and history review.
* **Appointment Operations**: Global oversight of all hospital appointments across all departments.
* **Session Audit Logs**: Comprehensive session tracking monitoring user logins, doctor activity, and administrative access times.
* **Inquiries & Feedback**: Review and respond to contact queries submitted via the public website.

---

### 🧪 Pathology & Diagnostic Laboratory Management
* **Dynamic Parameter Report Builder**: Create single and multi-test diagnostic panels (CBC, Biochemistry, Urine Routine, Lipid Profile, Liver Function Tests, etc.).
* **Standardized Single-Page A4 Engine**: Guaranteed clinical A4 layout generator ensuring all test parameters, biological reference intervals, and doctor notes fit on one page.
* **Human-Readable Clinical Typography**: Standardized typography hierarchy (12pt section banners, 10.5pt bold test results, 9.5pt reference ranges, 8pt registration numbers).
* **Automated QR Code Report Verification**: Dynamically renders scannable QR codes on every report for instant digital authenticity verification.
* **Pathologist Signature & Branding Customization**: Master template customization supporting dynamic lab logos, header branding, and pathologist digital signatures.
* **Instant PDF & Print Export**: Integrated high-resolution PDF download engine for digital archival and official printing.

---

## Technology Stack

| Layer | Technology / Framework |
| :--- | :--- |
| **Backend Language** | Python |
| **Database Engine** | MySQL / MariaDB |
| **Web Server** | Apache (XAMPP / WAMP / LAMP) |
| **Frontend Framework** | HTML5, CSS3, JavaScript (ES6), Bootstrap 3.x |
| **Icons & Fonts** | FontAwesome 4.x, Google Fonts (Roboto, Outfit) |
| **Integrations** | QuickChart QR Code API, WhatsApp Universal Web API |
| **PDF & Printing** | CSS A4 Media Engine / Native Print API |

---

## Installation & Setup Guide

### 1. Place Project Files
Place the project folder inside your local web server root directory (e.g., `d:\xampp\htdocs\hospital` for XAMPP).

### 2. Start Apache and MySQL Services
Open the **XAMPP Control Panel** and start both the **Apache** and **MySQL** modules.

### 3. Import System Database
1. Open your browser and navigate to `http://localhost/phpmyadmin`.
2. Create a new database named `hms`.
3. Select the `hms` database, click on the **Import** tab.
4. Choose the `hms.sql` file located in the database directory of the project and click **Go**.

### 4. Database Configuration
Verify the database connection settings in `hms/include/config.php`:

```php
<?php
define('DB_SERVER', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'hms');

$con = mysqli_connect(DB_SERVER, DB_USER, DB_PASS, DB_NAME);

if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
?>
