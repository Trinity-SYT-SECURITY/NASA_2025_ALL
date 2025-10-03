FROM python:3.9-slim

WORKDIR /app

# Copy the entire project first
COPY . .

# Set working directory to backend folder
WORKDIR /app/backend

# Install dependencies from backend requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "ultra_simple_api:app", "--host", "0.0.0.0", "--port", "8000"]