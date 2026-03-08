# fastapi-vllm-sentiment

Sentiment analysis powered by a **vLLM model server** running Falcon-RW-1B, with a fully separated frontend. Three servers working together — the production pattern for serving LLMs.

## Project Structure

```
sentiment_app_vllm/
├── server/
│   ├── main.py            ← Backend — JSON API, calls vLLM
│   └── start_server.sh    ← Start the FastAPI backend
├── client/
│   ├── index.html         ← Frontend — separate UI
│   └── start_client.sh    ← Serve the frontend
└── README.md
```

## How It Works — 3 Servers

```
Frontend (port 3000)          FastAPI (port 8000)           vLLM (port 8010)
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│  index.html      │          │  main.py         │          │                  │
│                  │  POST    │                  │  POST    │  Falcon-RW-1B    │
│  Type text       │          │                  │          │  model on GPU    │
│  [Analyze] ─────────────►  │  Builds prompt   ─────────► │                  │
│                  │  JSON    │  Sends to vLLM   │  JSON    │  Generates text  │
│  See result      │          │                  │          │                  │
│  POSITIVE  ◄─────────────  │  Parses response ◄───────── │  Returns output  │
│                  │          │  Returns JSON    │          │                  │
└──────────────────┘          └──────────────────┘          └──────────────────┘
```

| Server | Port | Role | What it does |
|--------|------|------|-------------|
| vLLM | 8010 | Model server | Runs the LLM on GPU |
| FastAPI (Uvicorn) | 8000 | API backend | Prompt engineering, parsing, returns JSON |
| Python HTTP Server | 3000 | Frontend | Serves static HTML/JS files |

## Setup

```bash
pip install fastapi uvicorn requests
```

## vLLM Setup

### What is vLLM?

vLLM is a high-performance model server for LLMs. It handles GPU memory management, batching, and optimization so your FastAPI app doesn't have to. Think of it as a separate engine that only does one thing — run the model.

### Step 1: Install vLLM

```bash
pip install vllm
```

**Requirements:** vLLM needs a CUDA-capable GPU (NVIDIA). Check your GPU with `nvidia-smi`. If you don't have a GPU, you can use the previous example (`fastapi-sentiment`) which runs on CPU.

### Step 2: Download and start the model

```bash
python -m vllm.entrypoints.api_server --model tiiuae/falcon-rw-1b --port 8010
```

The first time you run this, vLLM will **automatically download** the model from Hugging Face (~2.6GB for Falcon-RW-1B). This only happens once — the model is cached in `~/.cache/huggingface/` for future runs.

You'll see logs like:

```
INFO:     Loading model tiiuae/falcon-rw-1b...
INFO:     Model loaded successfully.
INFO:     Uvicorn running on http://0.0.0.0:8010
```

Wait until you see "Model loaded" before starting the other servers.

### Step 3: Test the model server

In a separate terminal, test that vLLM is working:

```bash
curl -X POST http://127.0.0.1:8010/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, my name is", "max_tokens": 10}'
```

You should get a JSON response with generated text.

### Using a different model

Just change the `--model` flag:

```bash
# Smaller model
python -m vllm.entrypoints.api_server --model facebook/opt-350m --port 8010

# Larger model (needs more GPU memory)
python -m vllm.entrypoints.api_server --model meta-llama/Llama-2-7b-hf --port 8010

# Qwen model
python -m vllm.entrypoints.api_server --model Qwen/Qwen2-1.5B --port 8010
```

No code changes needed in `main.py` — it just calls the same endpoint regardless of which model is running.

### Common vLLM flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--model` | Which model to load | `tiiuae/falcon-rw-1b` |
| `--port` | Which port to serve on | `8010` |
| `--gpu-memory-utilization` | Max GPU memory to use | `0.8` (80%) |
| `--max-model-len` | Max sequence length | `2048` |
| `--tensor-parallel-size` | Split across multiple GPUs | `2` (for 2 GPUs) |

## Run

```bash
# Terminal 1 — Start the vLLM model server first
python -m vllm.entrypoints.api_server --model tiiuae/falcon-rw-1b --port 8010
# Wait until model is loaded...

# Terminal 2 — Start the FastAPI backend
cd sentiment_app_vllm/server
bash start_server.sh

# Terminal 3 — Start the frontend
cd sentiment_app_vllm/client
bash start_client.sh
```

Open `http://localhost:3000/index.html` in your browser.

## The Code

### `main.py` — Backend JSON API (complete)

```python
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

class TextRequest(BaseModel):
    text: str

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
```

### `index.html` — Frontend (complete)

```html
<h2>Sentiment Analysis (vLLM)</h2>

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

    document.getElementById("result").innerHTML = "Analyzing... (waiting for LLM)";

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
            <p><b>Sentiment:</b> ${data.sentiment}</p>
        `;
    } catch (error) {
        document.getElementById("result").innerHTML = "Error: " + error;
    }
}
</script>
```

## API Endpoint

| Method | Endpoint    | Description          | Request Body       | Response                                    |
|--------|-------------|----------------------|--------------------|---------------------------------------------|
| POST   | `/analyze`  | Analyze sentiment    | `{"text": "..."}` | `{"text": "...", "sentiment": "POSITIVE"}` |

Test with curl:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

Or at `http://127.0.0.1:8000/docs`.

## Key Concepts

- **3-server architecture** — Frontend (port 3000) → FastAPI (port 8000) → vLLM (port 8010). Each server has one job
- **CORS middleware** — Needed because frontend (port 3000) and backend (port 8000) are different origins
- **`requests.post()`** — FastAPI calls vLLM using Python's HTTP library, just like the frontend calls FastAPI using `fetch()`
- **Prompt engineering** — The prompt is crafted to get a one-word answer: `"Do not explain. Only output one word."`
- **Output parsing** — LLMs don't always return clean output. The code extracts text after `"Answer:"` and maps to POSITIVE/NEGATIVE/UNKNOWN
- **`temperature: 0.0`** — Makes the model deterministic. Important for classification tasks
- **`max_tokens: 2`** — Limits response to 2 tokens since we only need one word

## The Request Chain

```
1. User clicks "Analyze" in browser
2. index.html sends fetch() POST to FastAPI (port 8000)
3. FastAPI builds a prompt and sends requests.post() to vLLM (port 8010)
4. vLLM runs the LLM and returns generated text
5. FastAPI parses the output and returns JSON to the browser
6. index.html displays the result
```

Each arrow is an HTTP request — the same protocol at every layer, just different servers.

## Why 3 Servers?

| Server | Can be replaced with | Without changing the others |
|--------|---------------------|---------------------------|
| Frontend (port 3000) | React, mobile app, Slack bot | Yes |
| FastAPI (port 8000) | Django, Express.js | Yes |
| vLLM (port 8010) | SGLang, TGI, Ollama, OpenAI API | Yes |

That's the power of separation — swap any layer independently. Want to use Qwen3-32B instead of Falcon? Just restart vLLM with a different `--model`. No code changes.

## How This Builds on Previous Examples

| #  | Example                        | Key Lesson                                    | AI Model? | Servers |
|----|--------------------------------|-----------------------------------------------|-----------|---------|
| 1  | fastapi-hello-world            | Your first endpoint                           | No        | 1       |
| 2  | fastapi-multipage-app          | Multiple pages, HTML embedded in Python       | No        | 1       |
| 3  | fastapi-templates              | HTML in separate files (Jinja2)               | No        | 1       |
| 4  | fastapi-login-demo             | Frontend-backend separation                   | No        | 2       |
| 5  | fastapi-routers                | Organizing a growing backend                  | No        | 1       |
| 6  | fastapi-crud                   | Full CRUD with all HTTP methods               | No        | 2       |
| 7  | fastapi-sentiment              | AI model inside FastAPI                       | Yes       | 2       |
| 8  | **fastapi-vllm-sentiment** ←   | AI model on separate vLLM server              | Yes       | 3       |
