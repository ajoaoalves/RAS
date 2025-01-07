FROM rabbitmq:3-management

# Update package list and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    --no-install-recommends && \
    pip3 install --break-system-packages pika && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the Python script into the container
COPY setup_queues.py /setup_queues.py

# Start RabbitMQ, wait for it to initialize, and run the setup script
CMD ["sh", "-c", "rabbitmq-server & sleep 10 && python3 /setup_queues.py && wait"]
