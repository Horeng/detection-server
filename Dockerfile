FROM python:3.11-slim

WORKDIR /app

# Copy all files to app directory
COPY . .

# Prepare execution environment and clone repository
# ------------------------------------------------------------
# 1) Install git and clear apt cache
# 2) Install pipenv and dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    $HOME/.local/bin/uv sync

# Prepare Python execution environment
# ------------------------------------------------------------
# 1) Set Python path (replace pipenv shell)
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
# ------------------------------------------------------------
# These variables are used in app.py
# and are set in run_on_local_server.yml
# ENV FLASK_HOST=0.0.0.0
# ENV FLASK_PORT=5000

# Run main script
CMD ["sh", "-c", "cd /app && python app.py -c /app/examples/kafka-dev.conf -m"]
