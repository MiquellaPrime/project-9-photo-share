# Project "PhotoShare"

## Development Setup

### Prerequisites
- Python 3.11+
- Poetry 2.1.3
- Docker and Docker Compose (optional, for containerized workflow)

### Initial Setup

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Configure environment variables:**
   Copy the template and adjust values in your local `.env` file:
   ```bash
   cp .env.template .env
   ```

   Minimum required configuration:
   ```
   # Required database settings
   DB__POSTGRES__HOST=localhost
   DB__POSTGRES__PORT=5432
   DB__POSTGRES__USER=your_username
   DB__POSTGRES__PASSWORD=your_password
   DB__POSTGRES__DBNAME=photoshare_db

   # Required for Docker Compose port mapping
   SERVER__PORT=8000
   ```

3. **Setup pre-commit hooks (IMPORTANT!):**
   ```bash
   poetry run pre-commit install
   ```

4. **Verify setup:**
   ```bash
   poetry run pre-commit run --all-files
   ```

## Running the Application (Local Development)

You can run the app locally using your own PostgreSQL or by starting only the database from Docker.

### Option A: Use local PostgreSQL
1. Ensure the database is reachable with your `.env` values.
2. Apply migrations:
   ```bash
   alembic upgrade head
   ```
3. Run the app:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open:
   - Docs: `http://localhost:8000/docs`

### Option B: Use Docker for the database only
1. Start only the database service:
   ```bash
   docker compose up -d db
   ```
2. Ensure your `.env` has:
   ```
   DB__POSTGRES__HOST=localhost
   DB__POSTGRES__PORT=5432
   ```
3. Apply migrations:
   ```bash
   alembic upgrade head
   ```
4. Run the app:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open:
   - Docs: `http://localhost:8000/docs`

## Running in Docker (Full Stack)

1. Ensure `.env` exists and includes database variables and `SERVER__PORT`:
   ```
   DB__POSTGRES__USER=your_username
   DB__POSTGRES__PASSWORD=your_password
   DB__POSTGRES__DBNAME=photoshare_db
   DB__POSTGRES__PORT=5432
   SERVER__PORT=8000
   ```
   Note: The app service sets `DB__POSTGRES__HOST=db` and `DB__POSTGRES__PORT=5432` internally.

2. Build and start:
   ```bash
   docker compose up --build -d
   ```

   The container entrypoint applies migrations automatically.

3. Check logs:
   ```bash
   docker compose logs -f app
   ```

4. Open:
   - Docs: `http://localhost:${SERVER__PORT}/docs`

5. Stop:

   Stop only:
   ```bash
   docker compose down
   ```
   Full removal (containers, networks, and volumes):
   ```bash
   docker compose down -v
   ```

## Environment Variables Reference

`.env.template` contains all required keys. For Docker Compose, `SERVER__PORT` must be set to expose the application on your host.
