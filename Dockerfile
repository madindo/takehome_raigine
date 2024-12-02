# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies from requirements.txt or using pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the environment variables from the .env file
ENV PYTHONUNBUFFERED 1

# Run the Python script manually (modify as per your need)
CMD ["python", "manual.py"]