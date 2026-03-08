# This file demonstrates a full CRUD (Create, Read, Update, Delete) API.
# CRUD maps to the four core HTTP methods: POST, GET, PUT, DELETE.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS middleware is required here because the frontend (port 3000) and backend
# (port 8000) run on different ports, making them different "origins" in the browser's view.
# Without this, the browser would block all fetch() calls from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---

# Book is used for CREATE (POST) requests. Both fields are required —
# you can't create a book without a title and author.
class Book(BaseModel):
    title: str
    author: str

# BookUpdate is a separate model used for UPDATE (PUT) requests.
# Why not reuse Book? Because partial updates should be allowed — you might want
# to change only the title without touching the author, or vice versa.
# Optional[str] = None means the field is not required. If it's not provided,
# it defaults to None, and the update logic checks before overwriting.
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

# --- In-memory "database" ---
# A plain Python dict keyed by integer ID acts as a fake database.
# This is simple and sufficient for a demo, but data is lost every time
# the server restarts. A real app would use SQLite, PostgreSQL, etc.
books_db = {
    1: {"id": 1, "title": "1984", "author": "George Orwell"},
    2: {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
}

# next_id is a simple counter for generating unique IDs.
# Using global is a known limitation — it's not thread-safe and resets on restart.
# In a real app, the database would handle ID generation automatically (e.g., auto-increment).
next_id = 3

# CREATE — Add a new book
@app.post("/books")
def create_book(book: Book):
    # global tells Python we want to modify the module-level next_id variable,
    # not create a new local one. Without this, Python would create a local variable
    # and the counter would never actually increment.
    global next_id
    new_book = {"id": next_id, "title": book.title, "author": book.author}
    books_db[next_id] = new_book
    next_id += 1
    return new_book

# READ — List all books
@app.get("/books")
def list_books():
    # books_db is a dict keyed by ID. We return just the values (the book dicts)
    # as a list so the client gets a JSON array, not an object with numeric keys.
    return list(books_db.values())

# READ — Get one book
# {book_id} is a path parameter — FastAPI extracts it from the URL and converts it
# to an int automatically. So GET /books/1 → book_id=1 (integer, not string).
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books_db:
        # HTTPException 404 signals "resource not found" — the standard HTTP response
        # for when a requested item doesn't exist. Raising it stops execution immediately.
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

# UPDATE — Modify a book (partial update supported)
@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    # Only update fields that were actually provided in the request.
    # If the client sends {"title": "New Title"} without author, we leave author unchanged.
    if book.title is not None:
        books_db[book_id]["title"] = book.title
    if book.author is not None:
        books_db[book_id]["author"] = book.author
    return books_db[book_id]

# DELETE — Remove a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    # dict.pop() removes the key and returns its value in one step,
    # so we can include the deleted book's title in the confirmation message.
    deleted = books_db.pop(book_id)
    return {"message": f"Deleted '{deleted['title']}'"}
