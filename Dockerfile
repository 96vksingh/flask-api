# Use the official Python base image
FROM python:3.9-slim

# Install OpenSSL and dependencies
RUN apt-get update && apt-get install -y \
    openssl \
    libssl-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy Swagger UI assets
COPY templates ./templates

# Copy the application code
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run the Flask app
CMD ["python", "main.py"]
