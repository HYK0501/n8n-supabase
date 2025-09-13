# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Docker-based setup that combines n8n (workflow automation platform) with Supabase (open-source Firebase alternative). The setup provides a complete self-hosted automation environment with database, authentication, and API services.

## Architecture

### Core Components

**n8n Service**: Custom-built container with Python and Git support for workflow automation
- Base image: `n8nio/n8n:latest`
- Enhanced with Python 3, pip, and Git
- Mounts: Python code directory, SSH keys, n8n data volume
- Port: 5678

**MCP Server**: FastMCP-based Model Context Protocol server for external integrations
- Custom Python FastAPI server using FastMCP framework
- Provides tools for external API integration (eBug search, arithmetic operations)
- Port: 9000
- Health check endpoint: `/mcp`
- Connected to n8n via `MCP_SERVER_URL=http://mcp-server:9000/mcp`

**Supabase Stack**: Complete backend-as-a-service platform including:
- **PostgreSQL Database** (`supabase/postgres:15.8.1.060`) - Primary data store with logical replication
- **Kong Gateway** (`kong:2.8.1`) - API proxy and routing (ports 8000/8443)
- **GoTrue Auth** (`supabase/gotrue:v2.177.0`) - Authentication service
- **PostgREST** (`postgrest/postgrest:v12.2.12`) - Auto-generated REST API
- **Realtime** (`supabase/realtime:v2.34.47`) - WebSocket subscriptions
- **Storage** (`supabase/storage-api:v1.25.7`) - File storage with transformations
- **Studio** (`supabase/studio:2025.06.30`) - Web-based dashboard
- **Edge Functions** (`supabase/edge-runtime:v1.67.4`) - Serverless Deno functions
- **Analytics** (`supabase/logflare:1.14.2`) - Log aggregation and analytics
- **Supavisor** (`supabase/supavisor:2.5.7`) - Connection pooler

### Key Integration Points

- n8n connects to Supabase via `SUPABASE_HOST=http://kong:8000`
- n8n connects to MCP Server via `MCP_SERVER_URL=http://mcp-server:9000/mcp`
- n8n uses Supabase API keys for database operations
- All services share the `supabase-network` Docker network
- Python code and SSH keys are mounted into n8n for external integrations

## Environment Configuration

The project uses environment variables defined in `.env` (copy from `.env.expample`):

### Critical Variables
- `POSTGRES_PASSWORD` - Database password (must be secure for production)
- `JWT_SECRET` - JWT signing key (minimum 32 characters)
- `ANON_KEY` / `SERVICE_ROLE_KEY` - Supabase API keys
- `PYTHON_CODE_PATH` - Host path to Python code directory
- `SSH_KEYS` - Host path to SSH key directory
- `N8N_VOLUME` - Host path for n8n data persistence

### MCP Server Variables
- `EPF_URL` - EPF API endpoint URL for eBug integration
- `TOKEN` - Authorization token for EPF API access

### Service URLs
- n8n UI: `http://localhost:5678`
- MCP Server: `http://localhost:9000/mcp`
- Supabase API: `http://localhost:8000`
- Supabase Studio: `http://localhost:3000`

## Common Commands

### Environment Setup
```bash
# Copy environment template
cp .env.expample .env

# Edit environment variables (required before first run)
# Update POSTGRES_PASSWORD, JWT_SECRET, path variables, EPF_URL, and TOKEN
```

### Docker Operations
```bash
# Start all services
docker compose up -d

# Start specific service (e.g., MCP server only)
docker compose up mcp-server -d

# View logs
docker compose logs -f [service_name]

# Stop services
docker compose down

# Complete reset (removes all data)
./reset.sh
```

### Database Management
The PostgreSQL database includes several initialization scripts in `volumes/db/`:
- `roles.sql` - User roles setup
- `jwt.sql` - JWT configuration
- `realtime.sql` - Realtime functionality
- `webhooks.sql` - Webhook triggers
- `logs.sql` - Analytics support

### Development Workflow

1. **Initial Setup**: Configure `.env` file with appropriate paths, secrets, and API credentials
2. **MCP Server Setup**: Ensure `EPF_URL` and `TOKEN` are configured for eBug API integration
3. **Custom n8n Workflows**: Access n8n at `localhost:5678` to create automation workflows
4. **Database Operations**: Use Supabase Studio at `localhost:3000` for database management
5. **Python Integration**: Place Python scripts in the mounted `PYTHON_CODE_PATH` directory
6. **SSH Access**: Configure SSH keys in the mounted `SSH_KEYS` directory for external integrations

### Volume Management

Persistent data is stored in `volumes/` directory:
- `volumes/db/data/` - PostgreSQL data (excluded from git)
- `volumes/storage/` - Supabase storage files (excluded from git)  
- `volumes/functions/` - Edge function source code
- `volumes/api/kong.yml` - Kong gateway configuration

The `reset.sh` script provides a complete environment reset, removing all containers, volumes, and data.

## MCP Server Configuration

The Model Context Protocol (MCP) server provides external API integration capabilities to n8n workflows.

### Available Tools
- **add**: Simple arithmetic addition of two integers
- **ebugcode**: Search eBug database by keyword with time range filtering
  - Parameters: `keyword` (string), `page_index` (int), `months_ago` (int)
  - Returns: JSON response with matching eBug entries

### Health Check
- Endpoint: `http://localhost:9000/mcp`
- Used by Docker health checks and service monitoring
- Returns 200 OK when server is healthy

### Integration with n8n
- n8n connects to MCP server via environment variable: `MCP_SERVER_URL=http://mcp-server:9000/mcp`
- Tools are accessible within n8n workflows for external data integration
- Requires proper authentication tokens configured in `.env` file

### Troubleshooting
1. Check `.env` file has `EPF_URL` and `TOKEN` configured
2. Verify port 9000 is not in use by other services
3. Review container logs: `docker compose logs -f mcp-server`
4. Test health endpoint: `curl -f http://localhost:9000/mcp`

### dev mcp server
1. `cd mcp_server`
2. `uv sync`
3. `uv run mcp server.py`
4. use `npx @modelcontextprotocol/inspector` run test