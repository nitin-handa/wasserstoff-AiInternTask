 # Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy project
COPY . .

# Expose the port Flask is running on
EXPOSE 5000

# Create uploads directory
RUN mkdir -p /app/src/static/uploads

# Define the default command
CMD ["python", "src/app.py"]

