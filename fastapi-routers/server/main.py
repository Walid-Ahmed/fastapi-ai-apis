# This file is the entry point for a FastAPI app that is split across multiple files.
# As an app grows, keeping all endpoints in one main.py becomes unmanageable.
# The router pattern solves this by letting each feature live in its own file.

from fastapi import FastAPI
# Each module (users, books) defines its own APIRouter instance with its own endpoints.
# Importing them here gives us access to those routers so we can plug them into the app.
from routers import users, books   # these are other files

app = FastAPI()

# app.include_router() registers all the routes defined in a router module into
# the main app. This is equivalent to having written all those @app.get() / @app.post()
# decorators directly in this file — it's just better organised.
# The main benefit: main.py stays small and is only responsible for wiring things together.
# Each router file is independently readable, testable, and editable.
app.include_router(users.router)
app.include_router(books.router)

# Why this pattern scales:
# Imagine 50 endpoints across users, books, auth, orders, and payments.
# Without routers, main.py becomes a 1000-line file.
# With routers, each feature file stays focused, and this file just wires them together.
