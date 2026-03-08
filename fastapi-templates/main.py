from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Home page with sign-in form
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Handle sign-in
@app.post("/signin", response_class=HTMLResponse)
def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        return templates.TemplateResponse("success.html", {
            "request": request,
            "username": username
        })
    return templates.TemplateResponse("error.html", {"request": request})
