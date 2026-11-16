#!/usr/bin/env bash
# scripts/setup.sh – One-shot development environment setup

set -euo pipefail

echo "=== Praxion – Development Setup ==="

# 1. Python virtual environment
echo "[1/5] Creating Python virtual environment..."
python -m venv .venv
source .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate

# 2. Install Python dependencies
echo "[2/5] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Copy env file
if [ ! -f .env ]; then
    echo "[3/5] Copying .env.example → .env  (fill in your secrets!)"
    cp .env.example .env
else
    echo "[3/5] .env already exists – skipping."
fi

# 4. Start Docker services
echo "[4/5] Starting Docker services (db, opa, otel-collector)..."
docker compose up -d db opa otel-collector

# 5. Run database migrations
echo "[5/5] Running Alembic migrations..."
sleep 3  # wait for postgres to be ready
cd backend && alembic upgrade head && cd ..

echo ""
echo "✅ Setup complete!"
echo "   Start backend : cd backend && uvicorn main:app --reload"
echo "   Start frontend: cd frontend && npm start"
echo "   Full stack    : docker compose up"
