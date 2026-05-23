# Use python 3.11 slim as the official base image
FROM python:3.11-slim

# Set system environment variables to prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system utilities needed for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency requirements file into the working directory
COPY requirements.txt .

# Install dependencies directly into the system environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source modules, notebooks, and verification tools
COPY src/ ./src/
COPY notebooks/ ./notebooks/
COPY verify_setup.py .

# Expose Jupyter interface port (8888) and Arize Phoenix trace collector port (6006)
EXPOSE 8888
EXPOSE 6006

# Start the Jupyter notebook interface server on container launch
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
