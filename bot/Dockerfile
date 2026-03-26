# Use Python 3.11 slim image
FROM python:3.11-slim

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY bot/pyproject.toml bot/uv.lock* ./

# Install dependencies (create lock file if not exists)
RUN uv sync --frozen 2>/dev/null || uv sync

# Copy bot source code
COPY bot/ .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["uv", "run", "bot.py"]
EOF