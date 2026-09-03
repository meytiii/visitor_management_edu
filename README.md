# Visitor management system (education office)

[![Version](https://img.shields.io/badge/version-3.2.4-blue.svg)](https://github.com/meytiii/visitor_management_edu)
[![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

Desktop application for managing visitor check-in and check-out across educational institutions and administrative complexes.

> **Archive notice:** This version is no longer supported. Development has moved to the [SQL Server version](https://github.com/meytiii/visitor_management_edu_sqlserver). This repository will not receive further updates.

---

## Features

- Role-based access control (admin and guard) with PBKDF2-SHA512 password hashing
- Visitor registration with auto-fill for returning visitors, Iranian national ID validation, and Persian name verification
- Thermal and standard receipt printing on Windows with customizable templates
- Search and pagination with filters for name, national ID, department, and Shamsi date, plus Excel export
- Analytics dashboard with daily traffic summaries and hourly heatmap charts
- Audit logging for logins, registrations, deletions, and database backups with Persian timestamps
- SQLite database backup and restore from `ProgramData`
- User management controls that prevent deleting the last remaining admin
- Right-to-left layout with a live Persian clock and cultural quotes
- Developer panel for test record generation, database cleanup, and audit log exports

---

## Tech stack

| Component | Technology |
| --- | --- |
| Language | Python 3.9+ |
| GUI framework | Tkinter, ttkbootstrap |
| Database | SQLite3 (WAL mode) |
| Calendar | jdatetime |
| Printing (Windows) | win32print, win32ui |
| Reporting | pandas, matplotlib |
| Text shaping | arabic_reshaper, python-bidi |
| Image processing | Pillow |

---

## Installation and setup

### End users

1. Download `VisitorSystem.exe` from the [Releases](https://github.com/meytiii/visitor_management_edu/releases) page.
2. Run the installer and follow the prompts.
3. Open **Visitor Management System**.
4. Sign in with the default credentials:
   - Username: `admin`
   - Password: `admin` (update this after your first login)

### Running from source

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/meytiii/visitor_management_edu.git
cd visitor_management_edu

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

### Building an executable

To generate a standalone Windows executable:

```bash
pyinstaller --noconsole --onefile --icon=assets/app_icon.ico --add-data "assets;assets" main.py
```
