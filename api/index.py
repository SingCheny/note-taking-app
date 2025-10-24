import sys
import os
from pathlib import Path

# Set up paths for module imports
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'

# Add both paths to ensure imports work
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

# Set environment variables for Vercel
os.environ.setdefault('VERCEL_ENV', 'production')
os.environ.setdefault('FLASK_ENV', 'production')

try:
    # Try to import the Flask app
    from main import app
    print("Successfully imported app from main")
except ImportError as e1:
    print(f"Failed to import from main: {e1}")
    try:
        from src.main import app
        print("Successfully imported app from src.main")
    except ImportError as e2:
        print(f"Failed to import from src.main: {e2}")
        # Create a minimal Flask app as fallback
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return f"""
            <h1>Flask App Status</h1>
            <p>Import Error 1: {e1}</p>
            <p>Import Error 2: {e2}</p>
            <p>Project Root: {project_root}</p>
            <p>Src Path: {src_path}</p>
            <p>Python Path: {sys.path}</p>
            """

# Vercel expects the Flask app to be available
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)