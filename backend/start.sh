#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head

# Initialize database with initial data
echo "Initializing database..."
python -c "from app.db.init_db import init_db; from app.db.session import SessionLocal; init_db(SessionLocal())"

# Start the application
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 