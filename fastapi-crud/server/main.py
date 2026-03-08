from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Book(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

# Fake database
books_db = {
    1: {"id": 1, "title": "1984", "author": "George Orwell"},
    2: {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
}

next_id = 3

# CREATE — Add a new book
@app.post("/books")
def create_book(book: Book):
    global next_id
    new_book = {"id": next_id, "title": book.title, "author": book.author}
    books_db[next_id] = new_book
    next_id += 1
    return new_book

# READ — List all books
@app.get("/books")
def list_books():
    return list(books_db.values())

# READ — Get one book
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

# UPDATE — Modify a book
@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
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
    deleted = books_db.pop(book_id)
    return {"message": f"Deleted '{deleted['title']}'"}
