
# FastAPI Demos

A collection of FastAPI examples, from basics to real-world patterns.

## Examples

### [fastapi-hello-world](./fastapi-hello-world)

The simplest FastAPI example — a single GET endpoint with a query parameter. Visit `/hello` for a default greeting or `/hello?name=Walid` for a personalized one. Introduces routing, query parameters, and JSON responses.

### [fastapi-login-demo](./fastapi-login-demo)

Frontend-backend separation with a login form. The frontend (HTML/JS) runs on port 3000 and communicates with the FastAPI backend (port 8000) using `fetch()`. Covers CORS setup, JSON request/response, and running two servers in development.

## Quick Start

```bash
pip install fastapi uvicorn
cd fastapi-hello-world
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` to explore the API.