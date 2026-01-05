#!/bin/bash

echo "🎨 Formatting code with Black..."
black app/

echo "🔍 Linting code with Flake8..."
flake8 app/ --max-line-length=88 --extend-ignore=E203,W503

echo "✅ Code quality check complete!"
