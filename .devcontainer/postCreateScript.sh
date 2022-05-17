#!/usr/bin/bash

POSTGRES_HOST="host.docker.internal"
POSTGRES_PORT="54321"

POSTGRES_DB="blog_db"
POSTGRES_USER="blog_user"
POSTGRES_PASSWORD="test123"

echo "Attempting to configure development database"
export PGPASSWORD=$POSTGRES_PASSWORD
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" a -f "./.devcontainer/setup/setUpDb.sql"


git config --global --add safe.directory /code