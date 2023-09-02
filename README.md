# midjourney-api (WIP)

Self-hostable unofficial API for Midjourney Discord bot

## Quickstart

1. Make a copy of `.env.template` and fill in the necessary credentials.

   ```bash
   cp .env.template .env
   vim .env 
   ```

2. Build and run the compose file, this will spin up a redis service (for task queue), a FastAPI server, and an ARQ worker.

    ```bash
    docker compose up --build
    ```

## Credit

<https://github.com/yokonsan/midjourney-api>
