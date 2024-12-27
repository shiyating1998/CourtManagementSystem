# Use a Python base image
FROM python:3.10-slim

# Set the environment variable for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /djangoApp

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    curl \
    redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements first to leverage Docker cache
COPY requirements.txt /djangoApp/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . /djangoApp/

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port
# EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]