# Dockerfile for FastAPI Backend (chatbot-openai)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (modular structure)
COPY config.py .
COPY models.py .
COPY openai_client.py .
COPY notifications.py .
COPY tools.py .
COPY app.py .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
