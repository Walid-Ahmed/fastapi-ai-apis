# fastapi-crud

A complete CRUD (Create, Read, Update, Delete) API for managing books, with a separate HTML frontend that uses all four HTTP methods via `fetch()`.

## Project Structure

```
fastapi-crud/
├── server/
│   ├── main.py            ← Backend — all CRUD endpoints
│   └── start_server.sh    ← Start the backend server
├── client/
│   ├── index.html         ← Frontend — book manager UI
│   └── start_client.sh    ← Serve the frontend
└── README.md
```

## Setup

```bash
pip install fastapi uvicorn
```

## Run

```bash
# Terminal 1 — Backend
cd fastapi-crud/server
bash start_server.sh

# Terminal 2 — Frontend
cd fastapi-crud/client
bash start_client.sh
```

Open `http://localhost:3000/index.html` in your browser.

## How It Works

```
Browser (localhost:3000)              Server (localhost:8000)
┌────────────────────────┐            ┌────────────────────────┐
│  index.html            │            │  main.py               │
│                        │  GET       │                        │
│  Page loads ──────────────────────► │  GET /books            │
│  Display book list ◄──────────────  │  → returns all books   │
│                        │            │                        │
│  [Add Book] ──────────────────────► │  POST /books           │
│                        │  POST      │  → creates new book    │
│                        │            │                        │
│  [Edit] → [Save] ────────────────► │  PUT /books/{id}       │
│                        │  PUT       │  → updates book        │
│                        │            │                        │
│  [Delete] ────────────────────────► │  DELETE /books/{id}    │
│                        │  DELETE    │  → removes book        │
└────────────────────────┘            └────────────────────────┘
```

## The Code

### `main.py` — Backend (complete)

```python
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
```

### `index.html` — Frontend (complete)

```html
<h2>Book Manager</h2>

<!-- Add Book Form -->
<h3>Add a Book</h3>
<input type="text" id="title" placeholder="Title">
<input type="text" id="author" placeholder="Author">
<button onclick="addBook()">Add Book</button>

<!-- Edit Book Form (hidden by default) -->
<div id="editSection" style="display:none;">
    <h3>Edit Book</h3>
    <input type="hidden" id="editId">
    <input type="text" id="editTitle" placeholder="Title">
    <input type="text" id="editAuthor" placeholder="Author">
    <button onclick="saveEdit()">Save</button>
    <button onclick="cancelEdit()">Cancel</button>
</div>

<!-- Book List -->
<h3>All Books</h3>
<button onclick="loadBooks()">Refresh List</button>
<div id="bookList"></div>

<script>
const API = "http://localhost:8000";

// CREATE — Add a new book (POST)
async function addBook() {
    try {
        const response = await fetch(`${API}/books`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                title: document.getElementById("title").value,
                author: document.getElementById("author").value
            })
        });
        const data = await response.json();
        alert(`Added: ${data.title} by ${data.author}`);
        document.getElementById("title").value = "";
        document.getElementById("author").value = "";
        loadBooks();
    } catch (error) {
        alert("Error: " + error);
    }
}

// READ — List all books (GET)
async function loadBooks() {
    try {
        const response = await fetch(`${API}/books`);
        const books = await response.json();
        const list = books.map(b =>
            `<p>${b.id}. <strong>${b.title}</strong> by ${b.author}
             <button onclick="startEdit(${b.id}, '${b.title}', '${b.author}')">Edit</button>
             <button onclick="deleteBook(${b.id})">Delete</button></p>`
        ).join("");
        document.getElementById("bookList").innerHTML = list || "<p>No books found</p>";
    } catch (error) {
        document.getElementById("bookList").innerHTML = "Error loading books";
    }
}

// UPDATE — Show edit form with current values
function startEdit(id, title, author) {
    document.getElementById("editSection").style.display = "block";
    document.getElementById("editId").value = id;
    document.getElementById("editTitle").value = title;
    document.getElementById("editAuthor").value = author;
}

// UPDATE — Save changes (PUT)
async function saveEdit() {
    const id = document.getElementById("editId").value;
    try {
        const response = await fetch(`${API}/books/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                title: document.getElementById("editTitle").value,
                author: document.getElementById("editAuthor").value
            })
        });
        const data = await response.json();
        alert(`Updated: ${data.title} by ${data.author}`);
        cancelEdit();
        loadBooks();
    } catch (error) {
        alert("Error: " + error);
    }
}

// UPDATE — Hide edit form
function cancelEdit() {
    document.getElementById("editSection").style.display = "none";
}

// DELETE — Remove a book (DELETE)
async function deleteBook(id) {
    try {
        const response = await fetch(`${API}/books/${id}`, {
            method: "DELETE"
        });
        const data = await response.json();
        alert(data.message);
        loadBooks();
    } catch (error) {
        alert("Error: " + error);
    }
}

// Load books on page load (automatic — no button click needed)
loadBooks();
</script>
```

## API Endpoints

| Method | Endpoint         | Description       | Request Body                             |
|--------|------------------|-------------------|------------------------------------------|
| GET    | `/books`         | List all books    | —                                        |
| GET    | `/books/{id}`    | Get one book      | —                                        |
| POST   | `/books`         | Add a new book    | `{"title": "", "author": ""}`            |
| PUT    | `/books/{id}`    | Update a book     | `{"title": ""}` or `{"author": ""}` or both |
| DELETE | `/books/{id}`    | Delete a book     | —                                        |

You can also test all endpoints at `http://127.0.0.1:8000/docs`.

## Frontend ↔ Backend Flow

| User Action            | Frontend Function | HTTP Method | Backend Endpoint      |
|------------------------|-------------------|-------------|-----------------------|
| Page opens             | `loadBooks()`     | GET         | `/books`              |
| Clicks "Add Book"      | `addBook()`       | POST        | `/books`              |
| Clicks "Edit"          | `startEdit()`     | — (no fetch, just shows form) | — |
| Clicks "Save"          | `saveEdit()`      | PUT         | `/books/{id}`         |
| Clicks "Delete"        | `deleteBook()`    | DELETE      | `/books/{id}`         |
| Clicks "Refresh List"  | `loadBooks()`     | GET         | `/books`              |

After every POST, PUT, and DELETE, the frontend calls `loadBooks()` again to refresh the list.

## Key Concepts

- **CRUD** — Create (POST), Read (GET), Update (PUT), Delete (DELETE) — the four basic operations for any resource
- **Path parameters** — `{book_id}` in the URL becomes a function argument. FastAPI converts it to `int` automatically
- **Pydantic models** — `Book` and `BookUpdate` define and validate what data the API expects
- **`Optional` fields** — `BookUpdate` lets you update just the title, just the author, or both
- **`HTTPException`** — Returns proper error codes (404 Not Found) instead of crashing
- **CORS middleware** — Required because frontend (port 3000) and backend (port 8000) are different origins
- **Auto-loading data** — `loadBooks()` at the bottom of the script runs on page load without any button click
- **Hidden form** — The edit section uses `display:none` and only appears when you click Edit
- **In-memory database** — The `books_db` dictionary acts as a fake database. Data resets when the server restarts

## Sample Responses

**GET /books**
```json
[
  {"id": 1, "title": "1984", "author": "George Orwell"},
  {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]
```

**POST /books** with `{"title": "Dune", "author": "Frank Herbert"}`
```json
{"id": 3, "title": "Dune", "author": "Frank Herbert"}
```

**PUT /books/1** with `{"title": "Nineteen Eighty-Four"}`
```json
{"id": 1, "title": "Nineteen Eighty-Four", "author": "George Orwell"}
```

**DELETE /books/1**
```json
{"message": "Deleted '1984'"}
```

**GET /books/99** (doesn't exist)
```json
{"detail": "Book not found"}
```

## How This Builds on Previous Examples

| Example                  | What it teaches                          | HTTP Methods           |
|--------------------------|------------------------------------------|------------------------|
| **fastapi-hello-world**  | Single endpoint, query parameters        | GET                    |
| **fastapi-multipage-app**| Multiple endpoints, HTML + forms         | GET, POST              |
| **fastapi-login-demo**   | Frontend-backend separation, CORS        | POST                   |
| **fastapi-routers**      | Splitting app into modules               | GET                    |
| **fastapi-crud** ←       | Full CRUD with separate frontend         | GET, POST, PUT, DELETE |
