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



# # Use Python slim image with apt-get support
# FROM python:3.9-slim-buster

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

# # Copy the application's requirements file to the working directory
# COPY requirements.txt ./

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install awslambdaric

# # Copy the current directory contents into the container
# COPY . .

# # Expose the port your app runs on
# # EXPOSE 4000

# # Command to run the application
# # CMD ["python3.9", "run.py"]
# # CMD ["run.lambda_handler"]

# CMD ["python3.9", "-m", "awslambdaric", "run.lambda_handler"]


# # CMD ["awslambdaric", "run.lambda_handler"]





# # Use Python slim image with apt-get support
# FROM python:3.9-slim-buster

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev curl && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

# # Install AWS Lambda Runtime Interface Emulator (RIE)
# RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
#     chmod +x /usr/local/bin/aws-lambda-rie

# # Copy the application's requirements file to the working directory
# COPY requirements.txt ./

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install awslambdaric

# # Copy the current directory contents into the container
# COPY . .

# # Command to run the application in AWS Lambda
# CMD ["aws-lambda-rie", "python3.9", "run.py"]









# FROM public.ecr.aws/lambda/python:3.9

# # Set the working directory in the container
# WORKDIR /var/task

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

# # Copy the application's requirements file to the working directory
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install awslambdaric awsgi

# # Copy the application code into the container
# COPY . .

# # Add the AWS Lambda Runtime Interface Emulator (RIE) for local testing
# # COPY --from=public.ecr.aws/lambda/python:3.9 /var/runtime/aws-lambda-rie /usr/local/bin/aws-lambda-rie

# # Command to run the Lambda function with RIE
# CMD ["run.lambda_handler"]
# # CMD ["python3.9", "-m", "awslambdaric", "run.lambda_handler"]




# # Use Amazon Linux 2 as the base image
# FROM amazonlinux:2

# # Install Python and necessary tools
# RUN yum install -y python3 python3-pip gcc libpq-devel && yum clean all

# # Set the working directory
# WORKDIR /var/task

# # Copy requirements.txt and install Python dependencies
# COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt
# RUN pip3 install --no-cache-dir awslambdaric awsgi

# # Copy the application code into the container
# COPY . .

# # Command to run the Lambda function
# CMD ["run.lambda_handler"]
