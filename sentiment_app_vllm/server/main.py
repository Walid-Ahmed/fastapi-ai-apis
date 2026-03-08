from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VLLM_ENDPOINT = "http://127.0.0.1:8010/generate"

# Request model
class TextRequest(BaseModel):
    text: str

# POST — Analyze sentiment via vLLM
@app.post("/analyze")
def analyze(request: TextRequest):
    prompt = (
        "Classify the sentiment of the following text as either POSITIVE or NEGATIVE.\n"
        "Do not explain. Only output one word.\n\n"
        f"Text: {request.text}\nAnswer:"
    )

    response = requests.post(
        VLLM_ENDPOINT,
        json={
            "prompt": prompt,
            "max_tokens": 2,
            "temperature": 0.0
        }
    )

    result = response.json()
    raw_output = result.get("text", [""])[0].strip()
    output = raw_output.split("Answer:")[-1].strip().upper()

    if "POS" in output:
        output = "POSITIVE"
    elif "NEG" in output:
        output = "NEGATIVE"
    else:
        output = "UNKNOWN"

    return {
        "text": request.text,
        "sentiment": output
    }
