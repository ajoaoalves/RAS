FROM python:3.8-slim-buster

WORKDIR /app

# Install minimal system dependencies for Pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .


CMD ["python", "border_tool_ms/main.py"]
