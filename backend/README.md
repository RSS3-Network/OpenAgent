# OpenAgent Backend

## Development

1 . Install dependencies

```bash
poetry shell
poetry install
```

2. Setup the database

```bash
docker compose up -d
```

3. Complete the environment variables

Copy the .env.example file to .env.local and fill in the environment variables.

4. Run the application

```bash
python main.py
```

### Add a New Expert

1. Add your Expert under [openagent/experts](./openagent/experts) with the logic to interact with external data sources and corresponding prompts. The directory contains some example Experts to get you started.
2. Add the Expert in [openagent/agent/function_agent.py](./openagent/agent/function_agent.py) to enable it, and you are done.

## Deployment

[Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml) provide a basic setup for deployment.

## Environment Variables

[.env.example](./.env.example) contains the environment variables required.
