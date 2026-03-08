# This file demonstrates serving an AI model through a FastAPI endpoint.
# The pattern here (load model at startup, expose a POST endpoint) is the standard
# way to deploy ML models as APIs.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# transformers is HuggingFace's library for working with pre-trained AI models.
from transformers import pipeline

app = FastAPI()

# CORS is needed because the frontend (port 3000) and backend (port 8000) are
# different origins. Without this, the browser blocks all fetch() requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The model is loaded HERE at module level — outside any function — so it runs ONCE
# when the server starts, not on every incoming request.
# Loading an ML model is expensive: it reads ~260MB from disk and allocates memory.
# If it were inside the analyze() function, every request would pay that cost,
# making the API unusably slow.
# On first run, pipeline() automatically downloads the default sentiment model
# (distilbert-base-uncased-finetuned-sst-2-english) from HuggingFace and caches it
# in ~/.cache/huggingface/. Subsequent runs load from cache — no download needed.
sentiment_model = pipeline("sentiment-analysis")

# Request model — Pydantic validates that the incoming JSON has a "text" field.
class TextRequest(BaseModel):
    text: str

# POST — Analyze sentiment
@app.post("/analyze")
def analyze(request: TextRequest):
    # sentiment_model() runs the text through the loaded model and returns a list
    # of results — one per input text. We only pass one string, so the list always
    # has one item. [0] extracts that single result dict.
    # A result looks like: {"label": "POSITIVE", "score": 0.9998}
    result = sentiment_model(request.text)[0]

    return {
        "text": request.text,
        "label": result["label"],   # "POSITIVE" or "NEGATIVE"
        # The model returns score as a probability between 0.0 and 1.0.
        # Multiplying by 100 converts it to a percentage (e.g., 0.9987 → 99.87).
        # round(..., 2) keeps two decimal places for a cleaner display value.
        "score": round(result["score"] * 100, 2)
    }
