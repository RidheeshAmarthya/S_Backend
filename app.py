from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db
from api_routes import api_bp
from admin_routes import admin_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sustainability_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
CORS(app)  # Enable CORS for API endpoints

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    """Redirect to admin dashboard"""
    return render_template('admin/index.html')

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

if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists('sustainability_db.sqlite'):
        init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5003)

