# FastAPI Tutorial Notes

A growing collection of notes, tips, and lessons learned while building FastAPI projects.

---

## 1. What is Uvicorn?

Uvicorn is a fast ASGI web server for Python. It's what runs your FastAPI app — it listens for HTTP requests and forwards them to your code.

- **Uvicorn is to Python** what **Node.js is to JavaScript**
- Both are event-loop driven and non-blocking
- For ML/AI serving, Python servers (Uvicorn) are the standard because the entire ML ecosystem lives in Python

### Basic usage

```bash
uvicorn main:app --reload
```

- `main` = your Python file name
- `app` = the FastAPI instance
- `--reload` = auto-restart when you save changes (development only)

### Production architecture

```
User's Browser
     ↓
Frontend (Vercel/Netlify) → serves HTML, CSS, JS
     ↓
Browser makes fetch() to API
     ↓
Nginx (reverse proxy) → handles SSL, load balancing
     ↓
Gunicorn (process manager) → manages multiple workers
     ↓
Uvicorn (worker) → runs your FastAPI code
     ↓
Database
```

---

## 2. Frontend vs Backend

### Backend code (FastAPI) handles

- Routing (`@app.get`, `@app.post`)
- Data validation (Pydantic models)
- Business logic (checking credentials, querying databases)
- Returning JSON responses

### Frontend code (HTML/JS) handles

- Displaying the UI (forms, buttons, pages)
- Collecting user input
- Sending requests to the backend via `fetch()`
- Showing results to the user

### Two approaches

**Monolithic** — Backend serves both HTML and data from one server:

```python
@app.get("/signin", response_class=HTMLResponse)
def signin_form():
    return "<form>...</form>"
```

**Separated** — Backend only serves JSON, frontend is a separate app:

```python
@app.post("/signin")
def signin(request: SignInRequest):
    return {"status": "success", "message": "Welcome!"}
```

The separated approach is the industry standard for production apps.

---

## 3. Running Two Servers in Development

In the separated approach, you need two terminals:

| Terminal | Command                      | Port | Role     |
|----------|------------------------------|------|----------|
| 1        | `uvicorn main:app --reload`  | 8000 | Backend  |
| 2        | `python -m http.server 3000` | 3000 | Frontend |

In PyCharm, click the `+` icon in the Terminal tab to open a second terminal.

**Important:** Make sure you `cd` into the correct project folder in **both** terminals before running commands.

### Killing old servers

```bash
kill -9 $(lsof -t -i :8000)
kill -9 $(lsof -t -i :3000)
```

If you get "not enough arguments," it means nothing was running — that's fine.

---

## 4. CORS (Cross-Origin Resource Sharing)

When the frontend (localhost:3000) tries to talk to the backend (localhost:8000), the browser blocks it because they're different origins. This is CORS.

### The fix

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow all origins (dev only)
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Key points

- Add CORS middleware **right after** `app = FastAPI()`
- Only create `app = FastAPI()` **once** in your file
- `"*"` is fine for development; use specific origins in production
- If you see `OPTIONS /signin 405`, CORS middleware isn't working
- Always restart the server after adding CORS (or use `--reload`)

---

## 5. GET vs POST (and Other HTTP Methods)

### The four main methods

| Method | Purpose                | Example               | Has request body? |
|--------|------------------------|-----------------------|-------------------|
| GET    | Read/fetch data        | `/books`, `/books/1`  | No                |
| POST   | Create something new   | `/books`              | Yes               |
| PUT    | Update existing item   | `/books/1`            | Yes               |
| DELETE | Remove something       | `/books/1`            | No                |

### GET in monolithic vs separated apps

In a **monolithic** app, GET can return HTML pages:

```python
@app.get("/signin", response_class=HTMLResponse)  # serves a form
```

In a **separated** app, GET only returns JSON data:

```python
@app.get("/books")  # returns JSON list
```

When frontend and backend are separated, you stop using GET to serve HTML. The frontend handles all pages. The backend only returns data via GET, POST, PUT, DELETE.

---

## 6. fetch() — How Frontend Talks to Backend

The JavaScript `fetch()` function sends HTTP requests from the browser to your API:

```javascript
const response = await fetch("http://localhost:8000/signin", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
        username: "admin",
        password: "1234"
    })
});
const data = await response.json();
```

### Handling responses

FastAPI returns different JSON shapes for success and error:

- Success: `{"status": "success", "message": "Welcome admin!"}`
- Error (HTTPException): `{"detail": "Invalid credentials"}`

Handle both:

```javascript
alert(data.message || data.detail || JSON.stringify(data));
```

Use `console.log(data)` to see the full response in the browser console (right-click → Inspect → Console).

---

## 7. APIRouter — Splitting Your App into Files

As your app grows, put each feature in its own file using `APIRouter`:

```python
# routers/books.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/books")
def list_books():
    return {"books": ["Book A", "Book B"]}
```

```python
# main.py
from fastapi import FastAPI
from routers import users, books

app = FastAPI()
app.include_router(users.router)
app.include_router(books.router)
```

`APIRouter` works exactly like `FastAPI()` but is designed to be plugged into a main app. Think of it as a mini-app for a specific feature.

---

## 8. Pydantic Models — Validating Request Data

Instead of using `Form(...)`, use Pydantic models for JSON APIs:

```python
from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
```

FastAPI automatically validates incoming JSON against these models. If someone sends `{"title": 123}`, FastAPI returns a validation error before your code even runs.

---

## 9. Common Errors and Fixes

### "Address already in use" (Errno 48)

An old server is still running on that port:

```bash
kill -9 $(lsof -t -i :8000)
```

### "OPTIONS /signin 405 Method Not Allowed"

CORS middleware is missing or not applied. Check that:

1. You have `CORSMiddleware` added right after `app = FastAPI()`
2. You only have **one** `app = FastAPI()` in the file
3. Uvicorn is running from the **correct folder** (check the log output)

### Alert shows "undefined"

The response JSON doesn't have the field you're looking for. Use:

```javascript
alert(data.message || data.detail || JSON.stringify(data));
```

### Uvicorn watching the wrong folder

Check the first line of Uvicorn's output — it shows which directory it's watching. Make sure you `cd` into the right folder before running `uvicorn main:app --reload`.

### "fatal: Authentication failed" on git push

GitHub no longer supports passwords. Use a Personal Access Token:

1. Go to `https://github.com/settings/tokens`
2. Generate new token (classic), check **repo** scope
3. Use the token as your password when pushing

---

## 10. FastAPI Free Features

- **`/docs`** — Auto-generated interactive API docs (Swagger UI). Test all endpoints in the browser
- **`/redoc`** — Alternative API docs with a different layout
- **JSON validation** — Pydantic models validate request data automatically
- **Type conversion** — Path parameters like `{book_id}: int` are converted automatically

---

## 11. Project Progression

| #  | Example                  | What it teaches                          | HTTP Methods          |
|----|--------------------------|------------------------------------------|-----------------------|
| 1  | fastapi-hello-world      | Single endpoint, query parameters        | GET                   |
| 2  | fastapi-multipage-app    | Multiple endpoints, HTML + forms         | GET, POST             |
| 3  | fastapi-login-demo       | Frontend-backend separation, CORS        | POST                  |
| 4  | fastapi-routers          | Splitting app into modules               | GET                   |
| 5  | fastapi-crud             | Full CRUD operations on a resource       | GET, POST, PUT, DELETE|