# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="ahsaan-abbasi"
# Set the working directory in the container
WORKDIR /code
# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# copy pyproject.toml file to add dependencies first
COPY pyproject.toml /code/

# Configuring the poetry environment for the project is not be created by default
RUN poetry config virtualenvs.create false

# install dependencies
RUN poetry Install

COPY . /code/

EXPOSE 8081

CMD [ "poetry", "run", "uvicorn", "app.main:app" "--host", "0.0.0.0", "--port", "8081", "--reload"]
