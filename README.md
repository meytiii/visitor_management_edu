# 🛡️ Visitor Management System (Education Office)

[![Version](https://img.shields.io/badge/version-3.2.4-blue.svg)](https://github.com/meytiii/visitor_management_edu)
[![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

**A professional desktop application for managing visitor check‑in/out, designed for educational organizations and administrative complexes.**

![Background Image](./assets/background.png)


> # 🚨 **IMPORTANT NOTICE** 🚨
>
> ## ⚠️ THIS VERSION IS NO LONGER SUPPORTED ⚠️
>
> **Development has moved to the new [SQL Server Version](https://github.com/meytiii/visitor_management_edu_sqlserver).**
>
> ### Please use the new repository for all future updates, features, and support.
>
> *This repository is archived and will not receive any further updates.*

---




## ✨ Key Features

- **🔐 Secure Authentication** – Role‑based access (Admin / Guard) with hashed passwords (PBKDF2-SHA512).
- **📝 Smart Visitor Registration** – Auto‑fill returning visitor info, Iranian national ID validation, Persian name validation.
- **🖨️ Receipt Printing** – Direct printing to thermal or standard printers (Windows) with customizable template.
- **🔎 Advanced Search & Pagination** – Filter by name, national ID, department, or Shamsi date. Export results to Excel.
- **📊 Analytics Dashboard** – Daily traffic reports and hourly heatmap charts.
- **📜 Comprehensive Audit Log** – Every action (login, register, delete, backup) is logged with Persian date.
- **🗄️ Backup & Restore** – One‑click backup/restore of the SQLite database from the hidden `ProgramData` folder.
- **👥 User Management** – Create/edit/delete users. Prevent deletion of the last admin.
- **🎨 Modern UI** – RTL layout, live Persian clock, rotating cultural messages.
- **🧑‍💻 Developer Mode** – Admin panel with test data generation, full DB cleanup, audit log export.

---

## 🛠️ Tech Stack

| Component       | Technology |
|----------------|------------|
| Language       | Python 3.9+ |
| GUI Framework  | Tkinter + `ttkbootstrap` |
| Database       | SQLite3 (WAL mode) |
| Persian Date   | `jdatetime` |
| Printing (Win) | `win32print` / `win32ui` |
| Reporting      | `pandas` + `matplotlib` |
| Text Reshaping | `arabic_reshaper` + `python-bidi` |
| Images         | Pillow (PIL) |

---

## 📥 Installation & Setup

### For End‑Users (no coding required)
1. Download the latest `VisitorSystem.exe` from the [Releases](https://github.com/meytiii/visitor_management_edu/releases) page.
2. Run the installer and follow the instructions.
3. Launch **Visitor Management System**.
4. Default admin credentials:
   - **Username:** `admin`
   - **Password:** `admin` *(change after first login)*

### For Developers (run from source)

```bash
# Clone the repository
git clone https://github.com/meytiii/visitor_management_edu.git
cd visitor_management_edu

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py```
```

### Build a Standalone EXE (optional)
```bash
pyinstaller --noconsole --onefile --icon=assets/app_icon.ico --add-data "assets;assets" main.py
```
