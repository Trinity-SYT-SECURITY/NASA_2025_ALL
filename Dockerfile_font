# Multi-stage build for Exoplanet AI Discovery Platform

# Stage 1: Build frontend
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build

# Stage 2: Setup backend
FROM python:3.9-slim as backend-setup

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Production image
FROM python:3.9-slim

WORKDIR /app

# Install nginx for static file serving
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend/ ./backend/
COPY --from=backend-setup /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-setup /usr/local/bin /usr/local/bin

# Copy frontend build
COPY --from=frontend-builder /app/frontend/build ./frontend/build/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directories for ML models
RUN mkdir -p ./ml

# Copy ML models (if they exist)
COPY ml/ ./ml/


# Set environment variables
ENV PYTHONPATH=/app
ENV ML_MODELS_PATH=/app/ml

# Expose ports
EXPOSE 80 8000

# Start script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
