# DFI Prospect Dashboard

A clean, monolithic Django web application for managing student prospect records at **Digital Fortress Institute**. Runs locally on `localhost` with zero authentication — anyone who accesses the dashboard URL has full CRUD access.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **Dashboard Table** — Paginated grid (15 rows/page) displaying all prospect fields side by side
- **Create & Edit** — Unified form for adding new records and updating existing ones
- **Safe Delete** — POST-only deletion with native browser `confirm()` prompt
- **Null Handling** — Missing fields render as stylized `—` placeholder tags instead of crashing
- **Seed Command** — Management command to bulk-import 328 email records from the included SQL backup
- **Zero Auth** — No login walls; full open access on localhost

---

## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Django 4.2 (Python 3.10+) |
| Database  | SQLite (`db.sqlite3`)   |
| Frontend  | HTML5, Vanilla CSS, Vanilla JS |
| Font      | [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts) |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/student_data.git
cd student_data
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Run database migrations

```bash
python3 manage.py migrate
```

### 5. Seed the database (optional)

Import the 328 existing email records from the included MariaDB backup file:

```bash
python3 manage.py seed_prospects
```

### 6. Start the development server

```bash
python3 manage.py runserver
```

### 7. Open the dashboard

Navigate to **[http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)** in your browser.

---

## Project Structure

```
student_data/
├── manage.py                              # Django management entry point
├── db.sqlite3                             # SQLite database (auto-created on migrate)
├── dfi_students_backup.sql                # Original MariaDB email backup (328 records)
├── README.md
│
├── student_data_project/                  # Django project config
│   ├── settings.py                        # App registration, DB config, timezone
│   ├── urls.py                            # Root URL routing (/dashboard/, / redirect)
│   ├── wsgi.py
│   └── asgi.py
│
└── prospects/                             # Core Django app
    ├── models.py                          # Prospect model (email + 7 optional fields)
    ├── views.py                           # Dashboard, create/edit form, delete handler
    ├── urls.py                            # 4 named routes (list, create, edit, delete)
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── management/
    │   └── commands/
    │       └── seed_prospects.py           # SQL backup importer
    └── templates/
        └── prospects/
            ├── dashboard.html             # Paginated table grid with actions
            └── prospect_form.html         # Unified create/edit form
```

---

## Data Model — `Prospect`

| Field            | Type        | Required | Notes                                          |
|------------------|-------------|----------|-------------------------------------------------|
| `email`          | EmailField  | ✅ Yes   | Unique, primary seed key                        |
| `full_name`      | CharField   | No       | Optional, nullable                              |
| `phone_number`   | CharField   | No       | Optional, nullable                              |
| `location`       | CharField   | No       | Optional, nullable                              |
| `occupation`     | CharField   | No       | Optional, nullable                              |
| `highest_degree` | CharField   | No       | Optional, nullable                              |
| `program`        | CharField   | No       | Optional, nullable                              |
| `how_heard`      | CharField   | No       | Dropdown: Roundabout Banner, Friends/Family, Traditional Media, Digital Advert, Fliers/Banner |
| `created_at`     | DateTime    | Auto     | Set automatically on record creation            |

---

## URL Routes

| URL Pattern                  | Method | Description              |
|------------------------------|--------|--------------------------|
| `/`                          | GET    | Redirects to `/dashboard/` |
| `/dashboard/`                | GET    | Paginated prospect table |
| `/dashboard/create/`         | GET/POST | Create new prospect    |
| `/dashboard/edit/<id>/`      | GET/POST | Edit existing prospect |
| `/dashboard/delete/<id>/`    | POST   | Delete prospect (with confirm) |

---

## Design Language

| Element                  | Color     |
|--------------------------|-----------|
| Background / Body        | `#FFF9F9` |
| Cards, Tables, Panels    | `#FFFFFF` |
| Primary Text             | `#0f172a` |
| Accent / Links           | `#3b82f6` |
| Danger / Delete          | `#ef4444` |
| Success Messages         | `#10b981` |

---

## License

This project is open source and available under the [MIT License](LICENSE).
