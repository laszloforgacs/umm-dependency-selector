# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Poetry
RUN apt-get update && apt-get install -y git && \
    apt install cloc=2.00 && \
    pip install --upgrade pip && \
    pip install poetry==1.8.2

# Configure Poetry:
# - Do not create a virtual environment inside the container
# - Install only dependencies without dev-dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Specify /config as a volume
VOLUME ["/usr/src/app/config"]

# Run the application
CMD ["poetry", "run", "python", "./main.py"]
