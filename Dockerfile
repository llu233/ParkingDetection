# Start with a Python base image
FROM python:3.8-slim

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y libopencv-dev

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python3", "app.py", "data/source/carPark.mp4", "data/source/CarParkPos"]