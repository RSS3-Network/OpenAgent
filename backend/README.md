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
