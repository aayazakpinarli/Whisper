# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ../requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
