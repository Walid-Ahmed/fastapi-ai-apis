#!/bin/bash

# Kill any process already using port 3000
PID=$(lsof -ti :3000)
if [ ! -z "$PID" ]; then
  echo "Killing process on port 3000 (PID: $PID)"
  kill -9 $PID
fi

# Serve static files
echo "Starting frontend on http://localhost:3000 ..."
python -m http.server 3000
