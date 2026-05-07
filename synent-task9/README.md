# Notely — A Simple Notes Web App

A small full-stack notes application built with **Flask + SQLite**. Users can sign up, log in, and manage their personal notes (create, view, edit, delete, search). Built as part of the **Synent Technologies Python Internship — Task 9 (Full Stack Project)**.

---

## Features

- User registration & login (sessions handled by Flask-Login)
- Passwords hashed with Werkzeug
- Create, view, edit, delete notes (each user only sees their own)
- Search notes by title or content
- Responsive UI — works on mobile and desktop
- Server-side validation + flash messages for feedback

---

## Tech Stack

| Layer    | Tool                       |
| -------- | -------------------------- |
| Backend  | Flask 3 (blueprints)       |
| ORM      | SQLAlchemy                 |
| Auth     | Flask-Login + Werkzeug     |
| Database | SQLite                     |
| Frontend | Jinja2 templates + custom CSS |

---

## Project Structure

```
synent-task9-notesapp-yourname/
├── app/
│   ├── __init__.py        # app factory
│   ├── models.py          # User & Note models
│   ├── auth/routes.py     # register / login / logout
│   ├── notes/routes.py    # CRUD + search
│   ├── main/routes.py     # landing page
│   ├── static/css/style.css
│   └── templates/         # Jinja2 templates
├── instance/              # SQLite DB lives here (gitignored)
├── config.py
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/synent-task9-notesapp-yourname.git
cd synent-task9-notesapp-yourname
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
cp .env.example .env
```

Then open `.env` and change `SECRET_KEY` to a long random string. You can generate one with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the app

```bash
python run.py
```

Open your browser at **http://127.0.0.1:5000**.

The SQLite database (`instance/notes.db`) is created automatically on first run.

---

## Routes Overview

| Method | Path                    | Description                 | Auth |
| ------ | ----------------------- | --------------------------- | ---- |
| GET    | `/`                     | Landing page                | No   |
| GET/POST | `/auth/register`      | Register new user           | No   |
| GET/POST | `/auth/login`         | Log in                      | No   |
| GET    | `/auth/logout`          | Log out                     | Yes  |
| GET    | `/notes/`               | List notes (`?q=` to search) | Yes  |
| GET/POST | `/notes/new`          | Create note                 | Yes  |
| GET    | `/notes/<id>`           | View a single note          | Yes  |
| GET/POST | `/notes/<id>/edit`    | Edit note                   | Yes  |
| POST   | `/notes/<id>/delete`    | Delete note                 | Yes  |

---

## Example User Flow

1. Visit `/` → see the landing page
2. Click **Sign up**, register with username/email/password
3. Log in with username **or** email
4. You're redirected to **My Notes**
5. Click **New** → write a note → save
6. Use the search bar to filter by title or content
7. Open a note → edit or delete it

---

## Notes for Reviewers

- Database file is created on first run inside `instance/` (gitignored).
- Each note is tied to a user via `user_id` foreign key, so users can never see or modify another user's notes (`abort(403)` on attempt).
- Password hashing uses `werkzeug.security` — plain passwords are never stored.
- The `SECRET_KEY` defaults to a placeholder for dev only; **always set a real one in production via `.env`**.

---

## Screenshots

> Add screenshots of the landing page, login screen, and notes dashboard here before pushing to GitHub.

---

## Author

Built by **yourname** for the Synent Technologies internship.

LinkedIn: _your-link-here_
