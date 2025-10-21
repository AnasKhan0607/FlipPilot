# API Service

FastAPI HTTP API server that provides REST endpoints for the FlipPilot application.

## What it does

- Serves HTTP API endpoints for the frontend
- Handles CORS for cross-origin requests
- Provides health check endpoints
- Manages communication with the agents service

## Prerequisites

- Python 3.11+
- FastAPI and dependencies installed

## Quick Start

1. **Install dependencies**:
   ```bash
   cd services/api
   pip install -r requirements.txt
   ```

2. **Start the API server**:
   ```bash
   uvicorn flippilot_api.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - Interactive docs: http://localhost:8000/docs

## Files

- `main.py` — FastAPI application with CORS middleware
- `routes/` — API route definitions (to be added)
