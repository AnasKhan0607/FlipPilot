# Services

This directory contains the backend services for FlipPilot.

## Services Overview

- **`api/`** — FastAPI HTTP API server
- **`agents/`** — LangGraph workers using RQ (Redis Queue) for background processing
- **`shared/`** — Common schemas, utilities, and shared code

## Quick Start

1. **Start Redis** (required for agents):
   ```bash
   docker run --rm -p 6379:6379 redis:7
   ```

2. **Start API server**:
   ```bash
   cd services/api
   # Follow api/README.md
   ```

3. **Start agents worker**:
   ```bash
   cd services/agents
   # Follow agents/README.md
   ```

## Development

Each service has its own README with specific setup instructions. The services communicate via Redis queues and HTTP APIs.
