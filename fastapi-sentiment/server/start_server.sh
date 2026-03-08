#!/bin/bash

# Kill any process already using port 8000
PID=$(lsof -ti :8000)
if [ ! -z "$PID" ]; then
  echo "Killing process on port 8000 (PID: $PID)"
  kill -9 $PID
fi

# Start FastAPI backend (model loads at startup — may take a moment)
echo "Starting FastAPI sentiment backend on http://127.0.0.1:8000 ..."
echo "Note: The transformers model will load on first startup."
uvicorn main:app --reload --port 8000
