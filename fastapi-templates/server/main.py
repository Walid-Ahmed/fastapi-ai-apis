# This file demonstrates Jinja2 templates — the standard way to serve dynamic HTML
# from a FastAPI backend without embedding HTML strings inside Python code.

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Jinja2Templates points FastAPI to the folder containing .html template files.
# The path "templates" is relative to where uvicorn is started from (the server/ directory),
# not relative to this Python file. This means you must run uvicorn from inside server/,
# otherwise FastAPI won't find the templates folder.
templates = Jinja2Templates(directory="templates")

# Home page with sign-in form
# The Request object must be accepted as a parameter and passed to TemplateResponse.
# FastAPI's Jinja2 integration requires it so templates can access request data
# (e.g., URL path, cookies). If you omit it, TemplateResponse will raise an error.
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # TemplateResponse loads the named .html file, renders it with the context dict,
    # and returns it as an HTML response. {"request": request} is always required —
    # it's a FastAPI convention that passes the request object into the template context.
    return templates.TemplateResponse("home.html", {"request": request})

# Handle sign-in
@app.post("/signin", response_class=HTMLResponse)
def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    # Form(...) reads the field from the HTML form submission (POST body).
    # This requires python-multipart to be installed — without it, FastAPI raises a 422 error.
    if username == "admin" and password == "1234":
        # "username" is added to the context dict so the Jinja2 template can use
        # {{ username }} to display the logged-in user's name on the success page.
        # Variables must be explicitly passed in the context — templates cannot access
        # Python variables automatically.
        return templates.TemplateResponse("success.html", {
            "request": request,
            "username": username
        })
    # On failure, we render the error template with only the required request context.
    return templates.TemplateResponse("error.html", {"request": request})
