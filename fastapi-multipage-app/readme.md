# fastapi-multipage-app

A FastAPI app that serves multiple HTML pages and handles form submissions — all from a single file. This is a monolithic approach where the backend serves both the UI and the logic.

## Project Structure

```
fastapi-multipage-app/
├── server/
│   ├── main.py       ← Backend serves HTML pages + handles form POST
│   └── start.sh      ← Start the server
└── README.md
```

## The Code — `main.py`

```python
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Home</h2>
    <a href="/signin">Go to Sign In</a> | 
    <a href="/about">Go to About Page</a>
    """

@app.get("/signin", response_class=HTMLResponse)
def signin_form():
    return """
    <h2>Sign In</h2>
    <form action="/signin" method="post">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    """

@app.post("/signin")
def signin(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        return {"status": "success", "message": f"Welcome {username}!"}
    return {"status": "error", "message": "Invalid credentials"}

@app.get("/about", response_class=HTMLResponse)
def about():
    return """
    <h2>About Page</h2>
    <p>This is a simple FastAPI demo with multiple endpoints.</p>
    """
```

## Setup

```bash
pip install fastapi uvicorn
```

## Run

```bash
cd fastapi-multipage-app/server
bash start.sh
```

## Try It

| URL                              | What You See                     |
|----------------------------------|----------------------------------|
| `http://127.0.0.1:8000/`        | Home page with navigation links  |
| `http://127.0.0.1:8000/signin`  | Sign in form                     |
| `http://127.0.0.1:8000/about`   | About page                       |
| `http://127.0.0.1:8000/docs`    | Interactive API documentation    |

Log in with: **admin** / **1234**

## Key Concepts

- **`HTMLResponse`** — Tells FastAPI to return HTML instead of JSON, so the browser renders a page
- **`Form(...)`** — Extracts form data from a POST request (requires `pip install python-multipart`)
- **GET vs POST on `/signin`** — GET serves the form, POST processes the submission
- **Monolithic approach** — The backend serves both the HTML pages and handles the logic. Compare this with [fastapi-login-demo](../fastapi-login-demo) where frontend and backend are separated

## How This Differs from fastapi-login-demo

| Feature               | fastapi-multipage-app        | fastapi-login-demo              |
|-----------------------|------------------------------|---------------------------------|
| Frontend              | HTML embedded in Python      | Separate `index.html` file      |
| Servers               | One (port 8000)              | Two (port 8000 + 3000)         |
| Communication         | Browser form POST            | JavaScript `fetch()` + JSON     |
| CORS needed?          | No                           | Yes                             |
| Real-world pattern?   | Quick prototypes             | Production applications         |