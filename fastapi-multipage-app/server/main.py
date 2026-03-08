# FastAPI can serve raw HTML directly — useful for simple multi-page apps where
# you don't want a separate frontend server or template engine.
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# response_class=HTMLResponse tells FastAPI to send the returned string as HTML
# instead of wrapping it in JSON. Without this, FastAPI would JSON-encode the string
# and the browser would see a quoted string, not a rendered page.
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Home</h2>
    <a href="/signin">Go to Sign In</a> |
    <a href="/about">Go to About Page</a>
    """

# GET /signin serves the HTML form to the browser.
# The form's action="/signin" and method="post" means submitting it will trigger
# the POST handler below — both GET and POST share the same URL path but do
# different things. This is standard HTML form behaviour.
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

# POST /signin processes the submitted form data.
# Form(...) tells FastAPI to read the value from the request body as form-encoded
# data (application/x-www-form-urlencoded), NOT from the URL or JSON body.
# The ... (Ellipsis) means this field is required — no default value.
# Note: Form() requires the python-multipart package to be installed.
# Note: Credentials are hardcoded here for demo purposes only — never do this in production.
@app.post("/signin")
def signin(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        return {"status": "success", "message": f"Welcome {username}!"}
    return {"status": "error", "message": "Invalid credentials"}

# About page
@app.get("/about", response_class=HTMLResponse)
def about():
    return """
    <h2>About Page</h2>
    <p>This is a simple FastAPI demo with multiple endpoints.</p>
    """
