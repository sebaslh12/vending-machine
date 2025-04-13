FROM python:3.12.8-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Create directory for persistent data
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Volume for persistent storage
VOLUME ["/app/data"]

# Run the application
CMD ["python", "vending_machine.py"]