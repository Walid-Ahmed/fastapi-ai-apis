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

# Request model
class TextRequest(BaseModel):
    text: str

# POST — Analyze sentiment
@app.post("/analyze")
def analyze(request: TextRequest):
    result = sentiment_model(request.text)[0]
    return {
        "text": request.text,
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    }
