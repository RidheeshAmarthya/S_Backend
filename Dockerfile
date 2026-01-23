FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads/core-pillars uploads/strategies uploads/contributors

# Expose port
EXPOSE 5003

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5003", "--workers", "2"]
