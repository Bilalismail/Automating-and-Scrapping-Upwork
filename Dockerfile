# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the command to run your application
CMD ["python", "main.py"]
