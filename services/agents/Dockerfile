# FlipPilot Agents Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY services/agents/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the worker (code mounted via volume in docker-compose)
CMD ["python", "flippilot_agents/worker.py"]
