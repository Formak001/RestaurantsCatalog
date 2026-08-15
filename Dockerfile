FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed for compiling certain libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml first to cache the dependency installation layer
COPY pyproject.toml /app/

# Install the dependencies declared in pyproject.toml
# Using setuptools backend to build the workspace package
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# Copy the rest of the application files
COPY . /app/

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
