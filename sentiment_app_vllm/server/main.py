# This file demonstrates calling a separate vLLM model server from FastAPI.
# Instead of loading a model into the FastAPI process, the model runs in its own
# server (vLLM on port 8010) and FastAPI forwards requests to it.
# This is the production pattern for serving large language models.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# requests is the standard Python HTTP library for making outbound HTTP calls.
# FastAPI uses it here to call the vLLM server, just as the browser's fetch()
# is used to call this FastAPI server.
import requests

app = FastAPI()

# CORS middleware is required because the browser-based frontend (port 3000) calls
# this FastAPI backend (port 8000) from a different origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# VLLM_ENDPOINT is a module-level constant so it's defined in one place.
# If the vLLM server address ever changes (e.g., to a different host or port),
# you only change it here rather than hunting through function bodies.
VLLM_ENDPOINT = "http://127.0.0.1:8010/generate"

# Request model — Pydantic validates that the incoming JSON has a "text" field.
class TextRequest(BaseModel):
    text: str

# POST — Analyze sentiment via vLLM
@app.post("/analyze")
def analyze(request: TextRequest):
    # --- Prompt Engineering ---
    # LLMs are general-purpose text generators — they don't inherently know to return
    # just "POSITIVE" or "NEGATIVE". The prompt structure is what constrains the output:
    #   1. We state the task explicitly ("Classify the sentiment...")
    #   2. We constrain the format ("Only output one word")
    #   3. We end with "Answer:" — a completion cue that tells the model to fill in
    #      the label next, rather than continuing to explain or rephrase.
    # This technique of crafting input text to steer model output is called prompt engineering.
    prompt = (
        "Classify the sentiment of the following text as either POSITIVE or NEGATIVE.\n"
        "Do not explain. Only output one word.\n\n"
        f"Text: {request.text}\nAnswer:"
    )

    response = requests.post(
        VLLM_ENDPOINT,
        json={
            "prompt": prompt,
            # max_tokens=2 limits the model to generating at most 2 tokens.
            # "POSITIVE" and "NEGATIVE" are each one token in most tokenizers.
            # Keeping this low prevents the model from generating extra text beyond
            # the single word we asked for.
            "max_tokens": 2,
            # temperature=0.0 makes the model fully deterministic — it always picks
            # the highest-probability next token. This is critical for classification:
            # we want consistent, repeatable answers, not creative variation.
            "temperature": 0.0
        }
    )

    result = response.json()
    # vLLM returns generated text in a list under the "text" key.
    # [0] gets the first (and only) generated sequence.
    # .strip() removes any surrounding whitespace or newlines.
    raw_output = result.get("text", [""])[0].strip()

    # vLLM echoes the full prompt back in the output, then appends the generated text.
    # split("Answer:")[-1] discards everything up to and including "Answer:" so we
    # only have the generated label. [-1] means "last part after the final split" —
    # handles edge cases where "Answer:" might appear earlier in the prompt too.
    output = raw_output.split("Answer:")[-1].strip().upper()

    # We use partial matching ("POS" in output, "NEG" in output) rather than exact
    # equality because LLMs may generate slightly inconsistent casing, spacing, or
    # extra characters even with max_tokens=2. "POS" catches "POSITIVE", "POSITIVE.",
    # "pos", etc. This makes the parsing more robust to minor model variations.
    if "POS" in output:
        output = "POSITIVE"
    elif "NEG" in output:
        output = "NEGATIVE"
    else:
        # The UNKNOWN fallback handles any output that doesn't match either sentiment.
        # This is defensive — it ensures the API always returns a valid JSON response
        # even if the model produces unexpected output, rather than crashing or returning
        # garbled text.
        output = "UNKNOWN"

    return {
        "text": request.text,
        "sentiment": output
    }
