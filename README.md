# Project "PhotoShare"

A web application for sharing photos with capabilities for uploading, editing, and commenting on images.

## System Requirements

### Prerequisites
- Python 3.11 or higher
- Poetry 2.1.3
- PostgreSQL 13+ (optional, if using your own database)
- Docker and Docker Compose (optional, for containerized workflow)

### External Services
- Cloudinary (for image storage)

## Initial Setup

### 1. Install dependencies

```bash
poetry install
```

### 2. Configure environment variables

Copy the template and adjust values in your local `.env` file:

```bash
cp .env.template .env
```

Edit the `.env` file with the following required parameters:

#### PostgreSQL Database
```env
DB__POSTGRES__HOST=localhost
DB__POSTGRES__PORT=5432
DB__POSTGRES__USER=your_username
DB__POSTGRES__PASSWORD=your_password
DB__POSTGRES__DBNAME=photoshare_db
```

#### Server Configuration
```env
SERVER__PORT=8000
```

#### Cloudinary (required!)
Register at [Cloudinary](https://cloudinary.com/) and obtain credentials:
```env
CLOUDINARY__CLOUD_NAME=your_cloud_name
CLOUDINARY__API_KEY=your_api_key
CLOUDINARY__API_SECRET=your_api_secret
```

#### JWT Tokens (required!)
```env
JWT__SECRET=your_secret_key_min_32_chars
JWT__ALGORITHM=HS256
JWT__ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT__REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Important:** To generate a secure `JWT__SECRET`, use:
```bash
openssl rand -hex 32
```

#### First Administrator
```env
FIRST_ADMIN__EMAIL=admin@example.com
FIRST_ADMIN__PASSWORD=secure_admin_password
```

This user will be automatically created on first run.

### 3. Setup pre-commit hooks (IMPORTANT!)

```bash
poetry run pre-commit install
```

### 4. Verify setup

```bash
poetry run pre-commit run --all-files
```

## Running the Application (Local Development)

### Option A: Use local PostgreSQL

1. Ensure the database is reachable with your `.env` values
2. Apply migrations and create admin user:
   ```bash
   alembic upgrade head
   python -m src.bootstrap
   ```
3. Run the app:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open:
   - API Docs: http://localhost:8000/docs

### Option B: Use Docker for the database only

1. Start only the database service:
   ```bash
   docker compose up -d db
   ```

2. Ensure your `.env` has:
   ```env
   DB__POSTGRES__HOST=localhost
   DB__POSTGRES__PORT=5432
   ```

3. **Manually execute commands from prestart.sh:**
   ```bash
   # Apply migrations
   alembic upgrade head

   # Create first admin user
   python -m src.bootstrap
   ```

4. Run the app:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Open:
   - API Docs: http://localhost:8000/docs

## Running in Docker (Full Stack)

### 1. Preparation

Ensure the `.env` file contains all required variables (as described above).

**Important:** When running in Docker, `DB__POSTGRES__HOST` is automatically set to `db` (the Docker service name), so you can leave `localhost` in `.env` - it will be overridden.

### 2. Start

```bash
docker compose up -d
```

The container automatically executes the `prestart.sh` script, which:
- Applies all database migrations
- Creates the first administrator (if not exists)

### 3. Check logs

```bash
docker compose logs -f app
```

### 4. Access the application

- API Docs: http://localhost:8000/docs (or another port specified in `SERVER__PORT`)

### 5. Stop

Stop containers:
```bash
docker compose down
```

Full removal (containers, networks, and volumes):
```bash
docker compose down -v
```

**Warning:** Using `-v` will delete all data from the database!

## Environment Variables Reference

All requirement environment variables are described in `.env.template`.
