"""
Minimal Vercel entry point for debugging
"""
import sys
import os
from pathlib import Path

# Ensure we have the right paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# Simple Flask app for testing
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Note Taking App - Vercel Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .status { padding: 20px; margin: 20px 0; border-radius: 5px; }
            .success { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .info { background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        </style>
    </head>
    <body>
        <h1>🚀 Note Taking App</h1>
        
        <div class="status success">
            ✅ Vercel deployment successful!
        </div>
        
        <div class="status info">
            📋 App Status: Running in minimal mode for debugging<br>
            🔧 Environment: Vercel Production<br>
            🐍 Python Version: Available<br>
            📁 Project Root: Available
        </div>
        
        <h2>Next Steps:</h2>
        <ul>
            <li>✅ Basic Flask app is working</li>
            <li>🔄 Need to fix main app imports</li>
            <li>📝 Database and full features coming soon</li>
        </ul>
        
        <h3>API Test:</h3>
        <p><a href="/api/test">Test API Endpoint</a></p>
    </body>
    </html>
    """

@app.route('/api/test')
def api_test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'environment': 'vercel',
        'python_path': sys.path[:3]  # Show first 3 paths
    })

# Vercel compatibility
application = app

if __name__ == "__main__":
    app.run(debug=False)