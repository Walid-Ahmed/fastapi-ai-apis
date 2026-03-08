# fastapi-login-demo

A simple project demonstrating how frontend and backend communicate in a real-world web application.

## Project Structure

```
fastapi-login-demo/
├── main.py        ← Backend (FastAPI + Uvicorn)
├── index.html     ← Frontend (HTML + JavaScript)
└── README.md
```

## How It Works

The **backend** (FastAPI) handles data and logic — it receives requests, validates credentials, and returns JSON responses. The **frontend** (HTML/JS) handles the user interface — it displays a form, sends data to the backend using `fetch()`, and shows the result.

They run as two separate servers that talk to each other over HTTP.

```
Browser (localhost:3000)          Server (localhost:8000)
┌──────────────────────┐          ┌──────────────────────┐
│  index.html          │  fetch() │  main.py             │
│  ┌────────────────┐  │ ──────►  │  POST /signin        │
│  │ Username: admin │  │          │  Validate credentials│
│  │ Password: ****  │  │  ◄────── │  Return JSON         │
│  │ [Login]         │  │  JSON    │                      │
│  └────────────────┘  │          │  {"status":"success", │
│                      │          │   "message":"Welcome"}│
└──────────────────────┘          └──────────────────────┘
```

## API Endpoints

| Method | Endpoint    | Description            | Server         |
|--------|-------------|------------------------|----------------|
| GET    | /           | Welcome message        | localhost:8000 |
| POST   | /signin     | Authenticate a user    | localhost:8000 |
| GET    | /about      | App info               | localhost:8000 |
| GET    | /index.html | Login form (frontend)  | localhost:3000 |

You can test any **GET** endpoint directly in your browser, for example `http://localhost:8000/about` returns:

```json
{"app": "FastAPI Demo", "version": "1.0"}
```

You can also test all endpoints interactively at `http://localhost:8000/docs` — FastAPI generates this documentation page automatically.

## Setup

### Step 1: Install FastAPI and Uvicorn

```bash
pip install fastapi uvicorn
```

### Step 2: Create the Backend — `main.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SignInRequest(BaseModel):
    username: str
    password: str

class SignInResponse(BaseModel):
    status: str
    message: str

users_db = {
    "admin": "1234",
    "walid": "pass123"
}

@app.get("/")
def home():
    return {"message": "Welcome to the API"}

@app.post("/signin", response_model=SignInResponse)
def signin(request: SignInRequest):
    if request.username in users_db and users_db[request.username] == request.password:
        return {"status": "success", "message": f"Welcome {request.username}!"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/about")
def about():
    return {"app": "FastAPI Demo", "version": "1.0"}
```

### Step 3: Create the Frontend — `index.html`

```html
<form id="loginForm">
    <input type="text" id="username" placeholder="Username">
    <input type="password" id="password" placeholder="Password">
    <button type="submit">Login</button>
</form>

<script>
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const response = await fetch("http://localhost:8000/signin", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: document.getElementById("username").value,
                password: document.getElementById("password").value
            })
        });
        const data = await response.json();
        console.log(data);
        alert(data.message || data.detail || JSON.stringify(data));
    } catch (error) {
        alert("Error: " + error);
    }
});
</script>
```

## Running the Project

You need **two terminals** open (in PyCharm, click the `+` icon in the Terminal tab).

### Terminal 1 — Start the Backend

```bash
cd /path/to/fastapi-login-demo
uvicorn main:app --reload
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 2 — Start the Frontend

```bash
cd /path/to/fastapi-login-demo
python -m http.server 3000
```

You should see:

```
Serving HTTP on :: port 3000 (http://[::]:3000/)
```

### Open in Browser

- **Login form:** `http://localhost:3000/index.html`
- **API docs:** `http://localhost:8000/docs`
- **About endpoint:** `http://localhost:8000/about`

Log in with:

- Username: `admin`
- Password: `1234`

## Two Servers, Two Jobs

| Server              | Port | Role                        | What it serves         |
|---------------------|------|-----------------------------|------------------------|
| Uvicorn (FastAPI)   | 8000 | Backend — logic and data    | JSON API responses     |
| Python HTTP Server  | 3000 | Frontend — user interface   | Static files (HTML/JS) |

The frontend (localhost:3000) serves `index.html` to the browser. The JavaScript inside uses `fetch()` to send requests to the backend (localhost:8000). In production, these would be separate addresses like `www.myapp.com` and `api.myapp.com`.

## Troubleshooting

### "Address already in use" error

A previous server is still running. Kill it and restart:

```bash
kill -9 $(lsof -t -i :8000)
kill -9 $(lsof -t -i :3000)
```

### "OPTIONS /signin 405 Method Not Allowed"

This is a CORS error. Make sure `main.py` has the `CORSMiddleware` added right after `app = FastAPI()`. Also make sure you only have **one** `app = FastAPI()` in the file.

### Alert shows "undefined"

The backend returned an error. Use `data.message || data.detail || JSON.stringify(data)` in your alert to see the actual error. Also check the browser console (right-click → Inspect → Console).

### Uvicorn watching the wrong folder

Make sure you `cd` into the correct project folder before running `uvicorn main:app --reload`. Check the log output — it shows which directory it is watching.

## Key Concepts

- **Uvicorn** — The Python server that runs your FastAPI backend
- **CORS** — Browser security that blocks requests between different origins (localhost:3000 → localhost:8000). The `CORSMiddleware` tells the browser it's okay
- **fetch()** — JavaScript function that sends HTTP requests from the frontend to the backend
- **JSON** — The data format used to communicate between frontend and backend
- **`--reload`** — Uvicorn flag that auto-restarts the server when you save changes to your code
- **`/docs`** — FastAPI auto-generates interactive API documentation at this endpoint

## Test Credentials

| Username | Password |
|----------|----------|
| admin    | 1234     |
| walid    | pass123  |