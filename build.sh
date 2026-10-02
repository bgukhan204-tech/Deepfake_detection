#!/usr/bin/env bash
# Render Build Script for DeepShield AI

# Exit on error
set -o errexit

echo "[BUILD] Installing Python dependencies..."
pip install -r requirements.txt

# If npm is installed, build the React frontend SPA
if command -v npm &> /dev/null; then
  echo "[BUILD] Building React Frontend..."
  if [ -d "frontend" ]; then
    cd frontend
    npm install
    npm run build
    cd ..
  fi
fi

echo "[BUILD] Build complete!"
