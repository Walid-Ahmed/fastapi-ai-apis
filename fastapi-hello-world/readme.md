# fastapi-hello-world

The simplest FastAPI example — a single GET endpoint with a query parameter.

## Project Structure

```
fastapi-hello-world/
├── server/
│   ├── main.py       ← Single endpoint API
│   └── start.sh      ← Start the server
└── README.md
```

## The Code — `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello(name: str = "World"):
    return {"message": f"Hello {name}"}
```

## Setup

```bash
pip install fastapi uvicorn
```

## Run

```bash
cd fastapi-hello-world/server
bash start.sh
```

## Try It

| URL                                        | Response                          |
|--------------------------------------------|-----------------------------------|
| `http://127.0.0.1:8000/hello`              | `{"message": "Hello World"}`      |
| `http://127.0.0.1:8000/hello?name=Walid`   | `{"message": "Hello Walid"}`      |
| `http://127.0.0.1:8000/docs`               | Interactive API documentation     |

## Key Concepts

- **`@app.get("/hello")`** — Defines a GET route at `/hello`
- **`name: str = "World"`** — A query parameter with a default value. FastAPI reads it automatically from the URL
- **JSON response** — FastAPI converts the Python dictionary to JSON automatically
- **`/docs`** — Auto-generated interactive docs where you can test the endpoint