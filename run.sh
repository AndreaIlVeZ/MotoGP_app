#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run the FastAPI server with hot reload
echo "🏍️  Starting MotoGP App server..."
uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
