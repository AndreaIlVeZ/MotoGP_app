#!/bin/bash

echo "🧪 Running tests..."

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=html --cov-report=term

echo ""
echo "📊 Coverage report generated in htmlcov/index.html"
