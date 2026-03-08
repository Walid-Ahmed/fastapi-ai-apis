# fastapi-sentiment-separated

The same sentiment analysis app, but with **frontend and backend fully separated** — the industry-standard pattern. The backend serves a JSON API, and the frontend is a standalone HTML/JS app that calls it using `fetch()`.

## Project Structure

```
fastapi-sentiment/
├── server/
│   ├── main.py              ← Backend — JSON API + AI model
│   ├── start_server.sh      ← Start the backend server
│   └── templates/           ← Jinja2 templates (template-based variant)
│       ├── home.html
│       └── sentiment.html
├── client/
│   ├── index.html           ← Frontend — separate UI
│   └── start_client.sh      ← Serve the frontend
└── README.md
```

## How It Works

```
Frontend (localhost:3000)             Backend (localhost:8000)
┌────────────────────────┐            ┌─────────────────────────────┐
│  index.html            │            │  main.py                    │
│                        │            │                             │
│  [Enter text here...]  │  POST     │                             │
│  [Analyze] ──────────────────────► │  POST /analyze              │
│                        │  JSON      │  Runs sentiment model       │
│  Result:               │            │  pipeline("sentiment-analysis")
│  POSITIVE 99.87%  ◄──────────────  │  Returns JSON               │
│                        │            │  {"label":"POSITIVE",       │
│                        │            │   "score": 99.87}           │
└────────────────────────┘            └─────────────────────────────┘
```

## Compared to fastapi-sentiment (templates version)

| Feature               | fastapi-sentiment (templates)  | fastapi-sentiment-separated    |
|-----------------------|-------------------------------|-------------------------------|
| Frontend              | Jinja2 templates              | Separate HTML + JavaScript    |
| Servers               | 1 (port 8000)                 | 2 (port 8000 + 3000)         |
| Backend returns       | Rendered HTML                 | JSON                          |
| Communication         | Browser form POST             | JavaScript `fetch()` + JSON   |
| CORS needed?          | No                            | Yes                           |
| Real-world pattern?   | Quick prototypes              | Production applications       |

## Setup

```bash
pip install fastapi uvicorn transformers torch
```

## Run

```bash
# Terminal 1 — Backend (API + model)
cd fastapi-sentiment/server
bash start_server.sh

# Terminal 2 — Frontend
cd fastapi-sentiment/client
bash start_client.sh
```

Open `http://localhost:3000/index.html` in your browser.

## The Code

### `main.py` — Backend (complete)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
sentiment_model = pipeline("sentiment-analysis")

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(request: TextRequest):
    result = sentiment_model(request.text)[0]
    return {
        "text": request.text,
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    }
```

### `index.html` — Frontend (complete)

```html
<h2>Sentiment Analysis</h2>

<textarea id="text" rows="4" cols="50" placeholder="Enter text here..."></textarea><br><br>
<button onclick="analyze()">Analyze</button>

<div id="result"></div>

<script>
async function analyze() {
    const text = document.getElementById("text").value;
    if (!text) {
        alert("Please enter some text");
        return;
    }

    document.getElementById("result").innerHTML = "Analyzing...";

    try {
        const response = await fetch("http://localhost:8000/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();
        document.getElementById("result").innerHTML = `
            <h3>Result:</h3>
            <p><b>Text:</b> ${data.text}</p>
            <p><b>Sentiment:</b> ${data.label}</p>
            <p><b>Confidence:</b> ${data.score}%</p>
        `;
    } catch (error) {
        document.getElementById("result").innerHTML = "Error: " + error;
    }
}
</script>
```

## API Endpoint

| Method | Endpoint    | Description          | Request Body       | Response                                      |
|--------|-------------|----------------------|--------------------|-----------------------------------------------|
| POST   | `/analyze`  | Analyze sentiment    | `{"text": "..."}` | `{"text": "...", "label": "POSITIVE", "score": 99.87}` |

Test it at `http://127.0.0.1:8000/docs` or with curl:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

## Key Concepts

- **Separated architecture** — Frontend and backend are independent. The backend only returns JSON, never HTML
- **CORS middleware** — Required because frontend (port 3000) and backend (port 8000) are different origins
- **Pydantic model** — `TextRequest` validates that the request contains a `text` field
- **Model loaded at startup** — `sentiment_model = pipeline(...)` runs once when the server starts, not on every request
- **"Analyzing..." feedback** — The frontend shows a loading message while waiting for the model to respond
- **No templates needed** — No Jinja2, no `templates/` folder. The backend is purely a JSON API

## Why Separate?

This pattern lets you:

- **Swap the frontend** — Replace `index.html` with React, a mobile app, or let a third-party call your API. The backend doesn't change
- **Scale independently** — If the model is slow, add more backend servers without touching the frontend
- **Different teams** — Frontend and backend developers work independently

## Try These Examples

| Input | Expected Result |
|---|---|
| "I love this product!" | POSITIVE ~99% |
| "This is terrible" | NEGATIVE ~99% |
| "The movie was okay" | POSITIVE ~60-70% |
| "I'm not sure about this" | NEGATIVE ~70-80% |

## How This Builds on Previous Examples

| #  | Example                          | Key Lesson                              | AI? | Servers |
|----|----------------------------------|-----------------------------------------|-----|---------|
| 1  | fastapi-hello-world              | Your first endpoint                     | No  | 1       |
| 2  | fastapi-multipage-app            | Multiple pages, HTML in Python          | No  | 1       |
| 3  | fastapi-templates                | HTML in separate files (Jinja2)         | No  | 1       |
| 4  | fastapi-login-demo               | Frontend-backend separation             | No  | 2       |
| 5  | fastapi-routers                  | Organizing a growing backend            | No  | 1       |
| 6  | fastapi-crud                     | Full CRUD with all HTTP methods         | No  | 2       |
| 7  | fastapi-sentiment                | Serving an AI model (templates)         | Yes | 1       |
| 8  | **fastapi-sentiment-separated** ← | AI model with separated frontend       | Yes | 2       |
