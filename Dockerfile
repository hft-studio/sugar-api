# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . .

# Expose the port that the app runs on
EXPOSE 5000

# Define environment variables
ENV PORT=5000
ENV HOST=0.0.0.0

# Run the FastAPI server with Uvicorn
CMD ["uvicorn", "bots.api:app", "--host", "0.0.0.0", "--port", "5000"]