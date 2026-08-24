# Base Python runtime
FROM python:3.11-slim as base

# Prevent writing bytecode and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose server port
EXPOSE 8000

# Run with Gunicorn using Uvicorn workers, reading dynamic PORT variable with 8000 fallback
CMD ["sh", "-c", "gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --timeout 120"]