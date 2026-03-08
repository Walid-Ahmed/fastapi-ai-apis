# fastapi-routers

Splitting a FastAPI app into multiple files using **APIRouter**. Instead of putting all endpoints in one `main.py`, each feature gets its own file — the standard pattern for organizing real-world FastAPI projects.

## Project Structure

```
fastapi-routers/
├── server/
│   ├── main.py              ← App entry point, includes routers
│   ├── start.sh             ← Start the server
│   └── routers/
│       ├── __init__.py      ← Makes routers a Python package
│       ├── users.py         ← /users endpoint
│       └── books.py         ← /books endpoint
└── README.md
```

## The Code

### `main.py` — Connects everything together

```python
from fastapi import FastAPI
from routers import users, books

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
```

### `routers/users.py` — Handles user endpoints

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return {"users": ["Alice", "Bob"]}
```

### `routers/books.py` — Handles book endpoints

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/books")
def list_books():
    return {"books": ["Book A", "Book B"]}
```

## Setup

```bash
pip install fastapi uvicorn
```

## Run

```bash
cd fastapi-routers/server
bash start.sh
```

## Try It

| URL                              | Response                              |
|----------------------------------|---------------------------------------|
| `http://127.0.0.1:8000/users`   | `{"users": ["Alice", "Bob"]}`         |
| `http://127.0.0.1:8000/books`   | `{"books": ["Book A", "Book B"]}`     |
| `http://127.0.0.1:8000/docs`    | Interactive API documentation         |

## Key Concepts

- **`APIRouter`** — Works exactly like `FastAPI()` but is designed to be included into a main app. Think of it as a mini-app for a specific feature
- **`app.include_router()`** — Plugs a router into the main app, registering all its endpoints
- **`routers/` package** — A folder with an `__init__.py` that groups related endpoint files together

## Why Use Routers?

Imagine your app grows to 50 endpoints — users, books, auth, orders, payments. Without routers, `main.py` becomes a 1000-line mess. With routers, each feature lives in its own file, and `main.py` just wires them together.

## How This Builds on Previous Examples

| Example                  | What it teaches                          | File structure       |
|--------------------------|------------------------------------------|----------------------|
| **fastapi-hello-world**  | Single endpoint, query parameters        | 1 file               |
| **fastapi-multipage-app**| Multiple endpoints, HTML + forms         | 1 file               |
| **fastapi-login-demo**   | Frontend-backend separation, CORS        | 2 files (py + html)  |
| **fastapi-routers** ←    | Splitting a growing app into modules     | Multiple files       |
