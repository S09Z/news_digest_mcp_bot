FROM python:3.10-slim

# Set environment variables
ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Create app directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies (without venv inside container)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY news_digest_mcp_bot ./news_digest_mcp_bot
COPY .env ./

# Run the app
CMD ["poetry", "run", "python", "news_digest_mcp_bot/main.py"]
