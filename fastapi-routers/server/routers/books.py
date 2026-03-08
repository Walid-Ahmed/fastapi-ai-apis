# This file owns all book-related endpoints.
# Keeping book logic here means the users.py and main.py files are not affected
# when you add, remove, or change book endpoints.

from fastapi import APIRouter

# APIRouter creates a mini-router that can be plugged into the main FastAPI app.
# This lets us define book endpoints here without needing access to the app object.
router = APIRouter()

@router.get("/books")
def list_books():
    # Returns a hardcoded list for demonstration. In a real app this would query a database.
    return {"books": ["Book A", "Book B"]}
