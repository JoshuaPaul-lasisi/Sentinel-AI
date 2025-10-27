FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for pandas/numpy/scipy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libatlas-base-dev \
    liblapack-dev \
    libblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Copy the data directory
COPY data/ ./data/

# Expose the port for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]