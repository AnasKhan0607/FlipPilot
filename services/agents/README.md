# Agents Service

LangGraph-based workers that process background tasks using RQ (Redis Queue).

## What it does

- Runs LangGraph workflows for property analysis
- Processes tasks from the "deals" queue
- Handles property ingestion, valuation, and analysis pipelines

## Prerequisites

- Python 3.11+
- Redis server running
- Virtual environment activated

## Quick Start

1. **Install dependencies**:
   ```bash
   cd services/agents
   pip install -r requirements.txt
   ```

2. **Start Redis** (if not already running):
   ```bash
   docker run --rm -p 6379:6379 redis:7
   ```

3. **Start the worker**:
   ```bash
   python flippilot_agents/worker.py
   ```

The worker will listen for jobs on the "deals" queue and process them using LangGraph workflows.

## Files

- `worker.py` — RQ worker that processes background jobs
- `tasks.py` — Task definitions and pipeline orchestration
- `graph.py` — LangGraph workflow definitions
