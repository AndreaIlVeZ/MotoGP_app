# 🚀 Quick Reference Guide

## Essential Commands

### Setup (First Time Only)
```bash
./setup.sh
```

### Start Server
```bash
./run.sh
# or
source venv/bin/activate
uvicorn app.backend.main:app --reload
```

### Stop Server
```
CTRL + C
```

### URLs
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

### Virtual Environment
```bash
# Activate
source venv/bin/activate

# Deactivate
deactivate

# Verify active
which python
```

### Dependencies
```bash
# Install new package
pip install <package-name>

# Save to requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Database
```bash
# Create database
createdb motogp_db

# Test connection
python test_db_connection.py

# Connect with psql
psql motogp_db
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Run both
./lint.sh
```

### Testing
```bash
# Run tests
pytest

# With coverage
./test.sh
```

### Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Git
```bash
# Status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin main
```

## File Locations

- Environment: `.env`
- Dependencies: `requirements.txt`
- Backend: `app/backend/`
- Routes: `app/backend/routers/`
- Config: `app/backend/config.py`
- Database: `app/backend/db.py`

## Environment Variables

Required in `.env`:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/motogp_db
SECRET_KEY=your-secret-key
DEBUG=True
PORT=8000
```

## API Testing with curl

```bash
# Health check
curl http://localhost:8000/api/health

# Root
curl http://localhost:8000
```

## Troubleshooting

### Port in use
```bash
lsof -i :8000
kill -9 <PID>
```

### Database connection
```bash
# Check if PostgreSQL is running
brew services list

# Start PostgreSQL
brew services start postgresql@15
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Virtual environment
```bash
# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development Workflow

1. `source venv/bin/activate` - Activate environment
2. `./run.sh` - Start server
3. Make changes (auto-reload enabled)
4. Test endpoints at http://localhost:8000/docs
5. `./test.sh` - Run tests
6. `./lint.sh` - Check code quality
7. `git add . && git commit -m "..."` - Commit changes

## Useful Keyboard Shortcuts

- `CTRL+C` - Stop server
- `CTRL+D` - Exit terminal/deactivate venv
- `CTRL+L` - Clear terminal

## Next Steps Checklist

- [ ] Set up PostgreSQL
- [ ] Run `./setup.sh`
- [ ] Update `.env` with database credentials
- [ ] Test connection: `python test_db_connection.py`
- [ ] Start server: `./run.sh`
- [ ] Visit http://localhost:8000/docs
- [ ] Create your first model
- [ ] Add your first endpoint
- [ ] Write tests
