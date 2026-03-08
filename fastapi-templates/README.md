# fastapi-templates

Using **Jinja2 templates** to separate HTML from Python code. Instead of embedding HTML strings inside your Python functions, HTML lives in its own files inside a `templates/` folder. Jinja2 lets you inject dynamic data (like the username) into the HTML.

## Project Structure

```
fastapi-templates/
├── main.py               ← Backend — routes and logic
├── templates/
│   ├── home.html         ← Sign-in form
│   ├── success.html      ← Welcome page (shows username)
│   └── error.html        ← Login failed page
└── README.md
```

## Setup

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

## Run

```bash
kill -9 $(lsof -t -i :8000)
cd fastapi-templates
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser. Log in with **admin** / **1234**.

**Note:** Only one server needed here — FastAPI serves both the HTML pages and handles the form. No separate frontend server, no CORS needed.

## The Code

### `main.py` — Routes and logic

```python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/signin", response_class=HTMLResponse)
def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        return templates.TemplateResponse("success.html", {
            "request": request,
            "username": username
        })
    return templates.TemplateResponse("error.html", {"request": request})
```

### `templates/home.html` — Sign-in form

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sign In</title>
</head>
<body>
    <h2>Sign In</h2>
    <form action="/signin" method="post">
        <label>Username: <input type="text" name="username"></label><br><br>
        <label>Password: <input type="password" name="password"></label><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

### `templates/success.html` — Welcome page

```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h2>Welcome {{ username }}!</h2>
    <p>You have signed in successfully.</p>
    <a href="/">Back to Home</a>
</body>
</html>
```

### `templates/error.html` — Error page

```html
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h2>Login Failed</h2>
    <p>Invalid username or password.</p>
    <a href="/">Try Again</a>
</body>
</html>
```

## Key Concepts

- **`Jinja2Templates`** — Loads HTML files from the `templates/` directory
- **`templates.TemplateResponse`** — Renders an HTML template and sends it to the browser
- **`{{ username }}`** — Jinja2 syntax for inserting dynamic data into HTML. The value comes from the dictionary passed in `TemplateResponse`
- **`{"request": request}`** — FastAPI requires the `request` object in every template context
- **`Form(...)`** — Extracts form data from a POST request (requires `python-multipart`)
- **One server** — Unlike the separated approach, the backend serves everything. No CORS needed

## Why Templates?

Compare three ways of handling HTML:

| Approach | Where HTML lives | Example |
|---|---|---|
| **Embedded** (fastapi-multipage-app) | Inside Python strings | `return "<h2>Home</h2>"` |
| **Templates** (this project) ← | Separate `.html` files | `return templates.TemplateResponse("home.html", {...})` |
| **Separated** (fastapi-login-demo) | Completely separate app | Frontend on port 3000, backend on port 8000 |

Templates are the middle ground — HTML is out of your Python code (cleaner), but the backend still serves everything (simpler than full separation).

## Jinja2 Features (Preview)

Jinja2 can do much more than just `{{ variable }}`:

```html
<!-- Conditionals -->
{% if username == "admin" %}
    <p>You have admin access</p>
{% else %}
    <p>Standard user</p>
{% endif %}

<!-- Loops -->
{% for book in books %}
    <p>{{ book.title }} by {{ book.author }}</p>
{% endfor %}
```

These become useful as your templates get more complex.

## How This Builds on Previous Examples

| #  | Example                  | How frontend is handled                    |
|----|--------------------------|-------------------------------------------|
| 1  | fastapi-hello-world      | No frontend, just JSON                    |
| 2  | fastapi-multipage-app    | HTML strings embedded in Python           |
| 3  | **fastapi-templates** ←  | HTML in separate files using Jinja2       |
| 4  | fastapi-login-demo       | Fully separate frontend with `fetch()`    |
| 5  | fastapi-routers          | Splitting backend into modules            |
| 6  | fastapi-crud             | Full CRUD with separate frontend          |
