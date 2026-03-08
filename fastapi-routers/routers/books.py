from fastapi import APIRouter

router = APIRouter()

@router.get("/books")
def list_books():
    return {"books": ["Book A", "Book B"]}
