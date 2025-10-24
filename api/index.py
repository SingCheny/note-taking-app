import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app

# Vercel expects the Flask app to be available at module level
application = app

if __name__ == "__main__":
    app.run()