#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "🛡  Northern Shift Guard — starting up"
echo "--------------------------------------"

# ── Backend ──────────────────────────────────────────────────────────────────
echo "[1/2] Starting backend..."

cd "$ROOT"

# Activate venv if it exists, otherwise use system python
if [ -f "$ROOT/venv/bin/activate" ]; then
  source "$ROOT/venv/bin/activate"
fi

# Install deps if anything is missing
pip install -q -r "$ROOT/backend/requirements.txt"

cd "$ROOT/backend"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "   Backend PID $BACKEND_PID → http://localhost:8000"

# ── Frontend ─────────────────────────────────────────────────────────────────
echo "[2/2] Starting frontend..."

cd "$ROOT/frontend"

# Install node deps if node_modules is missing
if [ ! -d "node_modules" ]; then
  echo "   Installing npm packages..."
  npm install
fi

npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID $FRONTEND_PID → http://localhost:5173"

# ── Cleanup on Ctrl+C ────────────────────────────────────────────────────────
cleanup() {
  echo ""
  echo "Shutting down..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  exit 0
}
trap cleanup SIGINT SIGTERM

echo ""
echo "✅ Both servers running."
echo "   App  → http://localhost:5173"
echo "   API  → http://localhost:8000"
echo "   Docs → http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop."

wait
