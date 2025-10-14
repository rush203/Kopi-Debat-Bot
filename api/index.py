"""Vercel serverless function entry point."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Export the FastAPI app for Vercel
handler = app
