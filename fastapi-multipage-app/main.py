from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Home page
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Home</h2>
    <a href="/signin">Go to Sign In</a> | 
    <a href="/about">Go to About Page</a>
    """

# Sign in page
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

# About page
@app.get("/about", response_class=HTMLResponse)
def about():
    return """
    <h2>About Page</h2>
    <p>This is a simple FastAPI demo with multiple endpoints.</p>
    """
