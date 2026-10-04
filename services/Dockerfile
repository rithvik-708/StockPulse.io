FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for confluent-kafka and uv
RUN apt-get update && apt-get install -y librdkafka-dev gcc curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

# Copy project definition and lock file first for caching
COPY pyproject.toml uv.lock ./
# Install all dependencies directly into the system environment to avoid virtualenv issues in Docker
RUN uv pip install --system -r pyproject.toml

# Copy application source
COPY . .

# Pass python module path to run as env var or default to api
ENV APP_MODULE="api.main:app"
# We run uvicorn or python based on the service
CMD ["sh", "-c", "if [ \"$SERVICE_TYPE\" = \"fastapi\" ]; then uvicorn $APP_MODULE --host 0.0.0.0 --port 8000; else python $APP_MODULE; fi"]
