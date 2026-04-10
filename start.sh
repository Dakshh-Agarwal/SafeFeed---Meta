#!/bin/bash
set -e

echo "[STARTUP] Running inference.py (benchmark + LLM proxy calls)..."
python inference.py

echo "[STARTUP] Starting uvicorn web server on port 7860..."
exec uvicorn backend.app:app --host 0.0.0.0 --port 7860
