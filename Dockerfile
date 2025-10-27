FROM python:3.11-bullseye

# Set the working directory
WORKDIR /app

# Install system dependencies required for pandas/numpy/scipy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    libatlas-base-dev \
    liblapack-dev \
    libblas-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir -r requirements.txt --prefer-binary

# Copy the source code
COPY src/ ./src/

# Copy the data directory
COPY data/ ./data/

# Expose the port for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]