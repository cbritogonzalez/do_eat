# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY splitter.py .
COPY normalizer.py .
COPY main.py .
COPY savedata_AH.json .
COPY savedata_jumbo.json .

# Expose the port that the app runs on
EXPOSE 7171

# Command to run the application
CMD ["python", "main.py"]