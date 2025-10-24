import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Flexible imports for different environments
try:
    from src.models.user import db
    from src.routes.user import user_bp
    from src.routes.note import note_bp
    from src.models.note import Note
except ImportError:
    # Fallback for Vercel environment
    sys.path.insert(0, str(Path(__file__).parent))
    from models.user import db
    from routes.user import user_bp
    from routes.note import note_bp
    from models.note import Note
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')

# Database configuration - smart environment detection
VERCEL_ENV = os.environ.get('VERCEL_ENV')  # Vercel sets this automatically
DATABASE_URL = os.environ.get('DATABASE_URL')

if VERCEL_ENV or not DATABASE_URL:
    # Vercel environment or local development: Use SQLite
    # This avoids PostgreSQL driver compilation issues in serverless
    if VERCEL_ENV:
        # Vercel: Use in-memory database (temporary)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        print(f"🗄️  Using in-memory SQLite database (Vercel mode)")
    else:
        # Local development: Use file-based SQLite
        ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
        # ensure database directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
        print(f"🗄️  Using file-based SQLite database (Local mode)")
else:
    # Local production testing with PostgreSQL
    database_url = DATABASE_URL
    # Handle postgres:// vs postgresql:// URL schemes
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"🗄️  Using PostgreSQL database")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize migrations
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    # Print startup info - already printed above in database config
    
    print(f"🚀 Starting Flask app on http://localhost:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
