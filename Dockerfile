# Use an official Python slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATA_DIR /app/data
ENV OUTPUT_DIR /app/outputs
ENV LOG_DIR /app/logs

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p $DATA_DIR $OUTPUT_DIR $LOG_DIR

# Define volume for persistent data
VOLUME ["/app/data", "/app/outputs", "/app/logs"]

# Set entrypoint
ENTRYPOINT ["python", "main.py"]
