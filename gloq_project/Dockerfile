# Use official Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies with cleanup
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies first (better caching)
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --timeout=1000 -r requirements.txt

# Copy project files
COPY . /app/

# Copy and set permissions for build script BEFORE switching users
COPY build.sh /app/
RUN chmod +x /app/build.sh

# Create non-root user for security AFTER setting permissions
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run with build script
CMD ["/app/build.sh"]