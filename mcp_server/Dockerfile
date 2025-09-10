# Use official uv image with Debian base
FROM ghcr.io/astral-sh/uv:debian

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock .env ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY server.py ./

# Expose the port that the MCP server runs on
EXPOSE 9000

# Create logs directory
RUN mkdir -p /var/log

# Run the MCP server
CMD ["uv", "run", "python", "server.py"]