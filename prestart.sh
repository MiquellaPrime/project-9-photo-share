#!/usr/bin/env bash

set -e

echo "Run apply migrations..."
alembic upgrade head
echo "Migrations applied!"

echo "Bootstrapping admin user..."
python -m src.bootstrap

exec "$@"
