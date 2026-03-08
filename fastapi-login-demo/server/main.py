from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel

app = FastAPI()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins (fine for development)
    allow_methods=["*"],
    allow_headers=["*"],
)
# Data models
class SignInRequest(BaseModel):
    username: str
    password: str

class SignInResponse(BaseModel):
    status: str
    message: str

# Fake database
users_db = {
    "admin": "1234",
    "walid": "pass123"
}

# Routes
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