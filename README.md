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

2. **Setup pre-commit hooks (IMPORTANT!):**
   ```bash
   poetry run pre-commit install
   ```

3. **Verify setup:**
   ```bash
   poetry run pre-commit run --all-files
   ```

### Daily Development
After initial setup, pre-commit will run automatically on every commit. No additional commands needed.
