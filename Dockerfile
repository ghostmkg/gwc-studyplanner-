# ---------------------------------
# StudySync Dockerfile
# ---------------------------------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create non-root user and set permissions
RUN adduser --disabled-password --gecos '' studysync \
    && chown -R studysync:studysync /app
USER studysync

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "main.py"]
