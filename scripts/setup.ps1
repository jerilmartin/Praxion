#!/usr/bin/env pwsh
# scripts/setup.ps1 – Windows PowerShell development setup

Write-Host "=== Praxion – Development Setup ===" -ForegroundColor Cyan

# 1. Virtual environment
Write-Host "[1/5] Creating Python virtual environment..."
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Dependencies
Write-Host "[2/5] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Env file
if (-not (Test-Path ".env")) {
    Write-Host "[3/5] Copying .env.example -> .env"
    Copy-Item ".env.example" ".env"
} else {
    Write-Host "[3/5] .env already exists – skipping."
}

# 4. Docker
Write-Host "[4/5] Starting Docker services..."
docker compose up -d db opa otel-collector

# 5. Migrations
Write-Host "[5/5] Running Alembic migrations..."
Start-Sleep 5
Set-Location backend
alembic upgrade head
Set-Location ..

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "  Start backend : cd backend; uvicorn main:app --reload"
Write-Host "  Start frontend: cd frontend; npm start"
Write-Host "  Full stack    : docker compose up"
