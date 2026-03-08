from fastapi import FastAPI
from routers import users, books   # these are other files

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(books.router)
