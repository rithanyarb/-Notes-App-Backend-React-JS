# 📝 Notes App Backend (FastAPI + SQLite3)

This is the **backend** of the full-stack Notes application built with **FastAPI**. It provides a secure **JWT-authenticated** API and uses **SQLite3** for storing users and notes.

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python  v3.13.2 (Preferred 3.8+)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- SQLite3 (comes pre-installed with Python)

---

### ⚙️ Setup Instructions

```bash
# Navigate to the backend folder
cd react_fastapi/NotesApp

# Create a virtual environment
python -m venv env

# Activate the environment
env\Scripts\activate  # Windows
# OR
source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

### ▶️ Run the Server

```bash
# Start FastAPI server
uvicorn main:app --reload
#goes to default 8000 port
# Optional: specify a custom port
uvicorn main:app --reload --port 8001
```

📘 API Docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧰 Tech Stack

- **FastAPI**
- **SQLAlchemy** (ORM)
- **JWT Authentication**
- **Pydantic** (for validation)
- **SQLite3** (default DB, serverless)

---

## 📂 Project Structure

```
📁 NotesApp/
  ├── main.py          # Entry point
  ├── database.py      # DB connection setup
  ├── models.py        # SQLAlchemy models
  └── routers/
      ├── auth.py      # Login/Register routes
      ├── notes.py     # CRUD for notes
      └── user.py      # User operations (future)
```

---

## 🔑 API Endpoints

### Authentication

| Method | Endpoint       | Description            |
|--------|----------------|------------------------|
| POST   | `/auth/`       | Register new user      |
| POST   | `/auth/token/` | Get access token (JWT) |

### Notes

| Method | Endpoint                  | Description             |
|--------|---------------------------|-------------------------|
| GET    | `/notes/notes/`           | Get user notes          |
| POST   | `/notes/notes/`           | Create a new note       |
| PUT    | `/notes/notes/{note_id}/` | Update an existing note |
| DELETE | `/notes/notes/{note_id}/` | Delete a note           |

---

## 🗃️ Accessing SQLite3 Database

```bash
cd react_fastapi/NotesApp
sqlite3 notesapp.db
```

In SQLite shell:

```sql
.mode box
or .mode table or .mode list etc
SELECT * FROM users;
SELECT * FROM notes;
```

📝 Sample schema:

```sql
CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT UNIQUE, email TEXT, hashed_password TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, is_active BOOLEAN);

CREATE TABLE notes (note_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, content TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME, FOREIGN KEY(user_id) REFERENCES users(user_id));
```

---

## ✍️ Author

Made with ❤️ by **RB Rithanya**

---

## 📜 License

Free to use for personal and educational purposes.

---
