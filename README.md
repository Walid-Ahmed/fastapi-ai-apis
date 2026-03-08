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

### [fastapi-sentiment](./fastapi-sentiment)

An AI-powered sentiment analysis app with frontend and backend fully separated. The backend serves a pure JSON API using a Hugging Face model, and the frontend calls it using `fetch()`. The industry-standard pattern for serving AI models.

## Learning Path

| #  | Example                        | Key Lesson                                    | AI Model? | Servers |
|----|--------------------------------|-----------------------------------------------|-----------|---------|
| 1  | fastapi-hello-world            | Your first endpoint                           | No        | 1       |
| 2  | fastapi-multipage-app          | Multiple pages, HTML embedded in Python       | No        | 1       |
| 3  | fastapi-templates              | HTML in separate files (Jinja2)               | No        | 1       |
| 4  | fastapi-login-demo             | Frontend-backend separation (industry pattern)| No        | 2       |
| 5  | fastapi-routers                | Organizing a growing backend                  | No        | 1       |
| 6  | fastapi-crud                   | Full CRUD with all HTTP methods               | No        | 2       |
| 7  | fastapi-sentiment              | Serving an AI model with separated frontend   | Yes       | 2       |

## Quick Start

```bash
pip install fastapi uvicorn jinja2 python-multipart
cd fastapi-hello-world
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` to explore the API.

## For AI Examples

```bash
pip install transformers torch
```
