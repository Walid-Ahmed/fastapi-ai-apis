# This file owns all user-related endpoints.
# By isolating them here, the users feature can be read, edited, and tested
# independently — without touching main.py or any other feature file.

from fastapi import APIRouter

# APIRouter works exactly like FastAPI() but is designed to be included into a
# parent app. You define routes on it using the same decorators (@router.get, etc.),
# and include_router() in main.py registers them onto the real app at startup.
router = APIRouter()

# Endpoints on a router use @router.xxx instead of @app.xxx.
# The path prefix (if any) would be set in main.py when calling include_router().
# Here there's no prefix, so this endpoint is reachable at /users directly.
@router.get("/users")
def list_users():
    # Returns a hardcoded list for demonstration. In a real app this would query a database.
    return {"users": ["Alice", "Bob"]}
