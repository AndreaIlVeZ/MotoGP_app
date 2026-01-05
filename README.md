# 🏍️ MotoGP App

A full-stack application for MotoGP enthusiasts, built with FastAPI backend, modern frontend, and PostgreSQL database.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for frontend)

### 1. Initial Setup

Run the automated setup script:
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all Python dependencies
- Create `.env` file from template

### 2. Configure Environment

Edit `.env` file with your database credentials and other settings:
```bash
nano .env
```

### 3. Setup Database

Make sure PostgreSQL is running and create the database:
```bash
createdb motogp_db
```

Or using psql:
```sql
CREATE DATABASE motogp_db;
```

### 4. Start Development Server

```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
uvicorn app.backend.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📁 Project Structure

```
motogp_app/
├── app/
│   ├── backend/
│   │   ├── routers/       # API endpoints
│   │   ├── config.py      # Configuration settings
│   │   ├── db.py          # Database connection
│   │   ├── main.py        # FastAPI app
│   │   └── schemas.py     # Pydantic models
│   ├── frontend/          # Frontend application
│   └── infra/             # Infrastructure configs
├── .env                   # Environment variables (DO NOT COMMIT)
├── .env.example           # Environment template
├── .gitignore
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
└── run.sh                # Run script
```

## 🛠️ Development

### Virtual Environment

Activate:
```bash
source venv/bin/activate
```

Deactivate:
```bash
deactivate
```

### Install New Dependencies

```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Database Migrations

(Coming soon with Alembic)

### Testing

```bash
pytest
```

## 📝 API Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /docs` - Interactive API documentation

## 🔧 Configuration

Key environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `SECRET_KEY` | JWT secret key | - |
| `DEBUG` | Debug mode | True |
| `PORT` | Server port | 8000 |

## 📚 Tech Stack

### Backend
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
(To be implemented)

## 🤝 Contributing

This is a learning project for infrastructure and backend development.

## 📄 License

MIT License
