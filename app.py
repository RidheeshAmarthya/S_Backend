from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from models import db, FoundationalPrinciple
from api_routes import api_bp
from admin_routes import admin_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')

# Database configuration - supports both SQLite (local) and PostgreSQL (production)
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production: Use PostgreSQL (Render, Railway, etc. provide DATABASE_URL)
    # Convert postgres:// to postgresql+psycopg:// for psycopg3 (Python 3.13 compatible)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
    elif database_url.startswith('postgresql://'):
        # Already postgresql://, add psycopg driver
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development: Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sustainability_db.sqlite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
CORS(app)  # Enable CORS for API endpoints

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Initialize database tables on app startup (works with gunicorn)
# This runs when the module is imported, ensuring tables exist before first request
with app.app_context():
    try:
        db.create_all()
        # Check if database is empty and initialize sample data
        if FoundationalPrinciple.query.count() == 0:
            from init_data import init_sample_data
            init_sample_data()
    except Exception as e:
        # Log error but don't crash - tables might already exist or DB not ready yet
        print(f"Database initialization note: {e}")

@app.route('/')
def index():
    """Redirect to admin dashboard"""
    return redirect(url_for('admin.dashboard'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Import after app context to avoid circular imports
        from init_data import init_sample_data
        init_sample_data()

def create_tables():
    """Create database tables if they don't exist"""
    with app.app_context():
        db.create_all()
        # Check if database is empty (no foundational principles)
        if FoundationalPrinciple.query.count() == 0:
            from init_data import init_sample_data
            init_sample_data()

if __name__ == '__main__':
    # Initialize database on first run
    port = int(os.environ.get('PORT', 5003))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Create tables and initialize data
    create_tables()
    
    app.run(debug=debug, host='0.0.0.0', port=port)

