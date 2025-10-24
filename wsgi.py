"""
Simple Flask app entry point for Vercel
"""
import os
import sys
from pathlib import Path

# Ensure we can find our modules
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / 'src'))

# Environment setup
os.environ.setdefault('FLASK_ENV', 'production')

# Import the Flask app
try:
    from src.main import app
except ImportError:
    sys.path.insert(0, str(root_dir / 'src'))
    from main import app

# This is what Vercel will use
application = app
app = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))