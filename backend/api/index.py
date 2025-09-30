"""
Vercel Serverless Function for Exoplanet AI Platform Backend
"""

import sys
import os

# Add the parent directory to the Python path to import from the main backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from main import app

# Vercel expects the app to be exported as a module
handler = app
