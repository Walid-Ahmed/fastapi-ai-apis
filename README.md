# FastAPI AI APIs

A collection of hands-on FastAPI examples — from basic routing to serving deep learning and generative AI models as APIs.

## Examples

### [fastapi-hello-world](./fastapi-hello-world)

The simplest FastAPI example — a single GET endpoint with a query parameter. Visit `/hello` for a default greeting or `/hello?name=Walid` for a personalized one. Introduces routing, query parameters, and JSON responses.

### [fastapi-multipage-app](./fastapi-multipage-app)

A monolithic FastAPI app that serves multiple HTML pages and handles form submissions from a single file. Covers `HTMLResponse`, `Form()` data, and GET vs POST on the same route.

### [fastapi-templates](./fastapi-templates)

Using Jinja2 templates to separate HTML from Python code. HTML lives in a `templates/` folder with dynamic data injection using `{{ variable }}` syntax. The middle ground between embedded HTML and full frontend separation.

### [fastapi-login-demo](./fastapi-login-demo)

Frontend-backend separation with a login form. The frontend (HTML/JS) runs on port 3000 and communicates with the FastAPI backend (port 8000) using `fetch()`. Covers CORS setup, JSON request/response, and running two servers in development.

### [fastapi-routers](./fastapi-routers)

Splitting a FastAPI app into multiple files using `APIRouter`. Each feature (users, books) gets its own file, and `main.py` wires them together. The standard pattern for organizing real-world FastAPI projects.

### [fastapi-crud](./fastapi-crud)

A complete CRUD (Create, Read, Update, Delete) API for managing books, with a separate HTML frontend. Covers all four HTTP methods, `fetch()` calls, Pydantic models, path parameters, and error handling.

## Learning Path

| #  | Example                | Key Lesson                                    | Servers |
|----|------------------------|-----------------------------------------------|---------|
| 1  | fastapi-hello-world    | Your first endpoint                           | 1       |
| 2  | fastapi-multipage-app  | Multiple pages, HTML embedded in Python       | 1       |
| 3  | fastapi-templates      | HTML in separate files (Jinja2)               | 1       |
| 4  | fastapi-login-demo     | Frontend-backend separation (industry pattern)| 2       |
| 5  | fastapi-routers        | Organizing a growing backend                  | 1       |
| 6  | fastapi-crud           | Full CRUD with all HTTP methods               | 2       |

## Quick Start

```bash
pip install fastapi uvicorn jinja2 python-multipart
cd fastapi-hello-world
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` to explore the API.
