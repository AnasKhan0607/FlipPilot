# FlipPilot API Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY services/api/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run the API (code mounted via volume in docker-compose)
CMD ["uvicorn", "flippilot_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
