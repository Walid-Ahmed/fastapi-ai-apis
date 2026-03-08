# This file demonstrates a JSON API backend with CORS support, Pydantic data models,
# and proper HTTP error handling — the standard pattern for a real-world FastAPI backend.

# All imports at the top — clean, no duplicates.
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# One app instance. Having two app = FastAPI() calls (a common copy-paste bug)
# means the second one silently replaces the first, discarding any middleware or
# routes attached to it before the second assignment.
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) is a browser security mechanism.
# When the frontend runs on localhost:3000 and the backend runs on localhost:8000,
# the browser treats them as different "origins" and blocks requests by default.
# CORSMiddleware tells the browser to allow these cross-origin requests.
# allow_origins=["*"] permits all origins — fine for development, but in production
# you would list specific allowed domains (e.g., ["https://myapp.com"]).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---

# Pydantic BaseModel defines the shape and types of request/response data.
# FastAPI uses these models to automatically validate incoming JSON, convert types,
# and generate interactive documentation. If a required field is missing or the
# wrong type, FastAPI returns a 422 error before your function is even called.
class SignInRequest(BaseModel):
    username: str
    password: str

# response_model (used below on the route) tells FastAPI to validate and filter
# the response through this model before sending it to the client. This ensures
# only the declared fields are ever returned — useful for stripping internal data.
class SignInResponse(BaseModel):
    status: str
    message: str

# --- In-memory "database" ---
# A plain Python dict acts as a fake database for this demo.
# In a real app this would be replaced with a proper database query.
# Storing passwords as plain text is for demo purposes only — never do this in production.
users_db = {
    "admin": "1234",
    "walid": "pass123"
}

# --- Routes ---

@app.get("/")
def home():
    return {"message": "Welcome to the API"}

# response_model=SignInResponse means FastAPI will validate the returned dict against
# SignInResponse and strip any extra fields before sending the response.
@app.post("/signin", response_model=SignInResponse)
def signin(request: SignInRequest):
    # Because SignInRequest is a Pydantic model, FastAPI automatically parses and
    # validates the JSON body, so we access fields as attributes (request.username).
    if request.username in users_db and users_db[request.username] == request.password:
        return {"status": "success", "message": f"Welcome {request.username}!"}

    # HTTPException with status_code=401 (Unauthorized) signals that authentication failed.
    # Raising it immediately stops execution and sends a proper HTTP error response —
    # much cleaner than returning a dict with an error message, because the HTTP status
    # code tells clients (and tools like curl) that the request actually failed.
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/about")
def about():
    return {"app": "FastAPI Demo", "version": "1.0"}
