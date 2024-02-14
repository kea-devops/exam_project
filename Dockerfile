# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    supervisor \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copy the project files to the container
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of your application's code
COPY . /app
COPY ./entrypoint.sh /
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV IPBR_URL="https://ipbr.treeleaf.dev/ipbr"
ENV REDIS_URL="redis://redis:6379/0"
ENV DB_HOST="db"
ENV DB_NAME="db"
ENV DB_USER="postgres"

# Command to run the application
CMD ["sh", "/entrypoint.sh"]
