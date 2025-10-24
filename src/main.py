import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, send_from_directory, jsonify
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

# Debug print to understand what's happening
print(f"🔍 Environment Detection: VERCEL_ENV={VERCEL_ENV}, DATABASE_URL={'SET' if DATABASE_URL else 'NOT SET'}")

if VERCEL_ENV:
    # Vercel environment: Always use in-memory database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    print(f"🗄️  Using in-memory SQLite database (Vercel mode)")
elif DATABASE_URL:
    # Local production testing with PostgreSQL
    database_url = DATABASE_URL
    # Handle postgres:// vs postgresql:// URL schemes
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"🗄️  Using PostgreSQL database")
else:
    # Local development: Use file-based SQLite
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
    # ensure database directory exists (safe on read-only filesystems)
    db_dir = os.path.dirname(DB_PATH)
    use_file_db = True
    try:
        os.makedirs(db_dir, exist_ok=True)
    except OSError as e:
        # Errno 30 corresponds to read-only filesystem on some platforms
        if getattr(e, 'errno', None) == 30:
            print(f"⚠️ Could not create DB dir '{db_dir}': Read-only filesystem. Falling back to in-memory DB.")
            use_file_db = False
        else:
            raise

    if use_file_db:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
        print(f"🗄️  Using file-based SQLite database (Local mode)")
    else:
        # Fall back to in-memory DB to avoid startup crash in serverless/read-only envs
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        print(f"🗄️  Using in-memory SQLite database (fallback due to read-only FS)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize migrations
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()


@app.route('/api/health')
def health():
    """Simple health endpoint reporting DB mode (file/memory/external) and masked URI."""
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    mode = 'unknown'
    if not uri:
        mode = 'none'
    elif uri == 'sqlite:///:memory:':
        mode = 'memory'
    elif uri.startswith('sqlite:///'):
        mode = 'file'
    else:
        mode = 'external'

    masked = uri
    if mode == 'external' and isinstance(uri, str):
        try:
            # mask credentials in URI if present
            import re
            masked = re.sub(r':/*[^:@]+:([^@]+)@', ':/*<redacted>@', uri)
            masked = re.sub(r'://[^:@]+:([^@]+)@', '://<user>:<redacted>@', masked)
        except Exception:
            pass

    return jsonify({
        'status': 'ok',
        'db_mode': mode,
        'db_uri': masked
    })

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
