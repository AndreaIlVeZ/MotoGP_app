# Database Setup Guide

## PostgreSQL Installation

### macOS
```bash
# Using Homebrew
brew install postgresql@15
brew services start postgresql@15

# Or using Postgres.app
# Download from https://postgresapp.com/
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Database Creation

### Option 1: Using createdb command
```bash
createdb motogp_db
```

### Option 2: Using psql
```bash
# Connect to PostgreSQL
psql postgres

# Create database
CREATE DATABASE motogp_db;

# Create user (optional)
CREATE USER motogp_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE motogp_db TO motogp_user;

# Exit psql
\q
```

## Update Connection String

Edit `.env` file:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/motogp_db
```

## Database Migrations with Alembic

### Initialize Alembic (only once)
```bash
alembic init alembic
```

### Create a migration
```bash
alembic revision -m "create initial tables"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Verify Connection

Run this Python script to test connection:
```python
from app.backend.db import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Database connection successful!")
        print(f"PostgreSQL version: {result.fetchone()[0]}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

## Common Issues

### Port Already in Use
```bash
# Check what's running on port 5432
lsof -i :5432

# Stop PostgreSQL
brew services stop postgresql@15
```

### Connection Refused
- Ensure PostgreSQL is running
- Check firewall settings
- Verify host and port in `.env`

### Authentication Failed
- Check username and password in `.env`
- Verify user has database permissions
