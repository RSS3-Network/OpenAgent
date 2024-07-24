# OpenAgent

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [GPU Support](#gpu-support)

## Prerequisites

Before deploying OpenAgent, ensure you have:

* Docker and Docker Compose installed
* Git (for cloning the repository)
* (Optional) NVIDIA GPU with appropriate drivers for GPU support

## Deployment

Follow these steps to deploy OpenAgent:

1. Clone the repository:
   ```bash
   git clone https://github.com/RSS3-Network/OpenAgent
   cd OpenAgent
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and fill in the required variables (see [Configuration](#configuration) section).

3. Deploy the containers:
   
   For CPU-only deployment:
   ```bash
   docker compose up -d
   ```
   
   For deployment with GPU support (on compatible systems):
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
   ```

## Configuration

The `.env` file contains crucial configuration settings. Here are the key sections:

### Basic Configuration

- `ENV`: Set to either "dev" or "prod"
- `MODEL_NAME`: Specify the AI model to be used (e.g., "llama3")
- `LLM_API_BASE`: API base for LLM requests (default: http://ollama:11434)
- `DB_CONNECTION`: Database connection string

### AI Model Configuration

Choose and configure one of the following AI models:

- OpenAI (e.g., "gpt-4o" or "gpt-4o-mini")
- Google Gemini (e.g., "gemini-1.5-pro" or "gemini-1.5-flash")
- Google Vertex AI
- Local LLM (see compatible models [here](https://docs.rss3.io/guide/artificial-intelligence/openagent/compatible-models))

Set the corresponding API keys or project IDs as needed.

### Executors Configuration

- `RSS3_DATA_API` and `RSS3_SEARCH_API`: Endpoints for RSS3 network
- `RSS3_API_KEY`: Required for RSS3 APIs
- `SERPAPI_API_KEY`: Optional, for Search executor
- `NFTSCAN_API_KEY`: Optional, for NFT executor

### Chainlit Configuration

Configure OAuth for user authentication:

- `OAUTH_AUTH0_CLIENT_ID`
- `OAUTH_AUTH0_CLIENT_SECRET`
- `OAUTH_AUTH0_DOMAIN`
- `CHAINLIT_AUTH_SECRET`

Refer to the [.env.example](./.env.example) file for a complete list of environment variables and their descriptions.

## GPU Support

To enable GPU support:

1. Ensure NVIDIA GPU drivers are installed.
2. Install the Nvidia container toolkit. Follow the [Nvidia Container Toolkit Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).
3. Use the GPU-enabled deployment command mentioned in the [Deployment](#deployment) section.

