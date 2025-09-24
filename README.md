# Project "PhotoShare"

## Development Setup

### Prerequisites
- Python 3.11+
- Poetry 2.1.3

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

   Example configuration:
   ```
   # Required database settings
   DB__POSTGRES__HOST=localhost
   DB__POSTGRES__PORT=5432
   DB__POSTGRES__USER=your_username
   DB__POSTGRES__PASSWORD=your_password
   DB__POSTGRES__DBNAME=photoshare_db
   ```

3. **Setup pre-commit hooks (IMPORTANT!):**
   ```bash
   poetry run pre-commit install
   ```

4. **Verify setup:**
   ```bash
   poetry run pre-commit run --all-files
   ```

### Daily Development
After initial setup, pre-commit will run automatically on every commit. No additional commands needed.

### Running the Application

```bash
uvicorn src.main:app --reload
```
