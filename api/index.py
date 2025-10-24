import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment variable for Flask to find static files
os.environ.setdefault('FLASK_APP', 'app')

try:
    from src.main import app
except ImportError as e:
    # Fallback: try importing without src prefix
    print(f"Import error: {e}")
    sys.path.insert(0, str(project_root / 'src'))
    from main import app

# Vercel expects the Flask app to be available at module level
application = app

# For Vercel serverless
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == "__main__":
    app.run(debug=False)