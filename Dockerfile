# Use the official Python image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your Flask app runs on
EXPOSE 8000

# Define environment variable for Flask to run
ENV FLASK_APP=app.py

# Start the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
