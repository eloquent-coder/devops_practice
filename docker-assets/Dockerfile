# Multi-stage build for smaller production image
FROM python:3.12-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies for banking data processing
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY docker-assets/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the generator script from src directory
COPY src/generate_transactions.py .

# Create non-root user for security (banking best practice)
RUN groupadd -r datauser && useradd -r -g datauser datauser
RUN chown -R datauser:datauser /app

USER datauser

# Environment variables for configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default environment variables (can be overridden in Kubernetes)
ENV DRY_RUN=false
ENV TXN_COUNT=8
ENV TXN_WINDOW_DAYS=60

# Health check for container readiness
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pandas, pandera; print('Dependencies OK')" || exit 1

# Default command - can be overridden in Kubernetes Job
CMD ["python", "generate_transactions.py"]
