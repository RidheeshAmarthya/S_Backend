from flask import Blueprint, request, jsonify, send_from_directory
from models import db, FoundationalPrinciple, CorePillar, SustainabilityStrategy, Project, Contributor, Certification, Synergy
from werkzeug.utils import secure_filename
import os

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder=''):
    """Save uploaded file and return the relative URL"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join('uploads', folder, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        return f"/uploads/{folder}/{filename}"
    return None

# ==================== FOUNDATIONAL PRINCIPLES ====================

@api_bp.route('/foundational-principles', methods=['GET'])
def get_foundational_principles():
    """Get all foundational principles"""
    principles = FoundationalPrinciple.query.all()
    return jsonify([p.to_dict() for p in principles])

@api_bp.route('/foundational-principles/<int:principle_id>', methods=['GET'])
def get_foundational_principle(principle_id):
    """Get a specific foundational principle"""
    principle = FoundationalPrinciple.query.get_or_404(principle_id)
    return jsonify(principle.to_dict())

@api_bp.route('/foundational-principles', methods=['POST'])
def create_foundational_principle():
    """Create a new foundational principle"""
    data = request.json
    principle = FoundationalPrinciple(
        name=data.get('name'),
        description=data.get('description')
    )
    db.session.add(principle)
    db.session.commit()
    return jsonify(principle.to_dict()), 201

@api_bp.route('/foundational-principles/<int:principle_id>', methods=['PUT'])
def update_foundational_principle(principle_id):
    """Update a foundational principle"""
    principle = FoundationalPrinciple.query.get_or_404(principle_id)
    data = request.json
    principle.name = data.get('name', principle.name)
    principle.description = data.get('description', principle.description)
    db.session.commit()
    return jsonify(principle.to_dict())

@api_bp.route('/foundational-principles/<int:principle_id>', methods=['DELETE'])
def delete_foundational_principle(principle_id):
    """Delete a foundational principle (should be restricted in production)"""
    principle = FoundationalPrinciple.query.get_or_404(principle_id)
    db.session.delete(principle)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

# ==================== CORE PILLARS ====================

@api_bp.route('/core-pillars', methods=['GET'])
def get_core_pillars():
    """Get all core pillars"""
    principle_id = request.args.get('principle_id', type=int)
    query = CorePillar.query
    if principle_id:
        query = query.filter_by(foundational_principle_id=principle_id)
    pillars = query.all()
    return jsonify([p.to_dict() for p in pillars])

@api_bp.route('/core-pillars/<int:pillar_id>', methods=['GET'])
def get_core_pillar(pillar_id):
    """Get a specific core pillar"""
    pillar = CorePillar.query.get_or_404(pillar_id)
    return jsonify(pillar.to_dict())

@api_bp.route('/core-pillars', methods=['POST'])
def create_core_pillar():
    """Create a new core pillar"""
    data = request.json
    pillar = CorePillar(
        foundational_principle_id=data.get('foundational_principle_id'),
        name=data.get('name'),
        description=data.get('description'),
        text_content=data.get('text_content'),
        author=data.get('author'),
        image_url=data.get('image_url')
    )
    
    # Handle certifications
    if 'certification_ids' in data:
        certifications = Certification.query.filter(Certification.id.in_(data['certification_ids'])).all()
        pillar.certifications = certifications
    
    db.session.add(pillar)
    db.session.commit()
    return jsonify(pillar.to_dict()), 201

@api_bp.route('/core-pillars/<int:pillar_id>', methods=['PUT'])
def update_core_pillar(pillar_id):
    """Update a core pillar"""
    pillar = CorePillar.query.get_or_404(pillar_id)
    data = request.json
    pillar.name = data.get('name', pillar.name)
    pillar.description = data.get('description', pillar.description)
    pillar.text_content = data.get('text_content', pillar.text_content)
    pillar.author = data.get('author', pillar.author)
    pillar.image_url = data.get('image_url', pillar.image_url)
    
    if 'certification_ids' in data:
        certifications = Certification.query.filter(Certification.id.in_(data['certification_ids'])).all()
        pillar.certifications = certifications
    
    db.session.commit()
    return jsonify(pillar.to_dict())

@api_bp.route('/core-pillars/<int:pillar_id>', methods=['DELETE'])
def delete_core_pillar(pillar_id):
    """Delete a core pillar"""
    pillar = CorePillar.query.get_or_404(pillar_id)
    db.session.delete(pillar)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

@api_bp.route('/core-pillars/<int:pillar_id>/upload-image', methods=['POST'])
def upload_core_pillar_image(pillar_id):
    """Upload image for core pillar"""
    pillar = CorePillar.query.get_or_404(pillar_id)
    if 'image' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['image']
    image_url = save_uploaded_file(file, 'core-pillars')
    if image_url:
        pillar.image_url = image_url
        db.session.commit()
        return jsonify({'image_url': image_url}), 200
    return jsonify({'error': 'Invalid file type'}), 400

# ==================== SUSTAINABILITY STRATEGIES ====================

@api_bp.route('/sustainability-strategies', methods=['GET'])
def get_sustainability_strategies():
    """Get all sustainability strategies"""
    pillar_id = request.args.get('pillar_id', type=int)
    query = SustainabilityStrategy.query
    if pillar_id:
        query = query.filter_by(core_pillar_id=pillar_id)
    strategies = query.all()
    return jsonify([s.to_dict() for s in strategies])

@api_bp.route('/sustainability-strategies/<int:strategy_id>', methods=['GET'])
def get_sustainability_strategy(strategy_id):
    """Get a specific sustainability strategy"""
    strategy = SustainabilityStrategy.query.get_or_404(strategy_id)
    return jsonify(strategy.to_dict())

@api_bp.route('/sustainability-strategies', methods=['POST'])
def create_sustainability_strategy():
    """Create a new sustainability strategy"""
    data = request.json
    strategy = SustainabilityStrategy(
        core_pillar_id=data.get('core_pillar_id'),
        name=data.get('name'),
        description=data.get('description'),
        text_content=data.get('text_content'),
        author=data.get('author'),
        cost=data.get('cost'),
        performance_contribution=data.get('performance_contribution'),
        image_url=data.get('image_url')
    )
    
    # Handle synergies
    if 'synergy_ids' in data:
        synergies = Synergy.query.filter(Synergy.id.in_(data['synergy_ids'])).all()
        strategy.synergies = synergies
    
    db.session.add(strategy)
    db.session.commit()
    return jsonify(strategy.to_dict()), 201

@api_bp.route('/sustainability-strategies/<int:strategy_id>', methods=['PUT'])
def update_sustainability_strategy(strategy_id):
    """Update a sustainability strategy"""
    strategy = SustainabilityStrategy.query.get_or_404(strategy_id)
    data = request.json
    strategy.name = data.get('name', strategy.name)
    strategy.description = data.get('description', strategy.description)
    strategy.text_content = data.get('text_content', strategy.text_content)
    strategy.author = data.get('author', strategy.author)
    strategy.cost = data.get('cost', strategy.cost)
    strategy.performance_contribution = data.get('performance_contribution', strategy.performance_contribution)
    strategy.image_url = data.get('image_url', strategy.image_url)
    
    if 'synergy_ids' in data:
        synergies = Synergy.query.filter(Synergy.id.in_(data['synergy_ids'])).all()
        strategy.synergies = synergies
    
    db.session.commit()
    return jsonify(strategy.to_dict())

@api_bp.route('/sustainability-strategies/<int:strategy_id>', methods=['DELETE'])
def delete_sustainability_strategy(strategy_id):
    """Delete a sustainability strategy"""
    strategy = SustainabilityStrategy.query.get_or_404(strategy_id)
    db.session.delete(strategy)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

@api_bp.route('/sustainability-strategies/<int:strategy_id>/upload-image', methods=['POST'])
def upload_strategy_image(strategy_id):
    """Upload image for sustainability strategy"""
    strategy = SustainabilityStrategy.query.get_or_404(strategy_id)
    if 'image' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['image']
    image_url = save_uploaded_file(file, 'strategies')
    if image_url:
        strategy.image_url = image_url
        db.session.commit()
        return jsonify({'image_url': image_url}), 200
    return jsonify({'error': 'Invalid file type'}), 400

# ==================== PROJECTS ====================

@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project"""
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict())

@api_bp.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.json
    project = Project(
        project_name=data.get('project_name'),
        project_size=data.get('project_size'),
        project_address=data.get('project_address'),
        construction_type=data.get('construction_type'),
        project_type=data.get('project_type'),
        design_stage=data.get('design_stage')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project"""
    project = Project.query.get_or_404(project_id)
    data = request.json
    project.project_name = data.get('project_name', project.project_name)
    project.project_size = data.get('project_size', project.project_size)
    project.project_address = data.get('project_address', project.project_address)
    project.construction_type = data.get('construction_type', project.construction_type)
    project.project_type = data.get('project_type', project.project_type)
    project.design_stage = data.get('design_stage', project.design_stage)
    db.session.commit()
    return jsonify(project.to_dict())

@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

# ==================== CONTRIBUTORS ====================

@api_bp.route('/contributors', methods=['GET'])
def get_contributors():
    """Get all contributors"""
    contributors = Contributor.query.all()
    return jsonify([c.to_dict() for c in contributors])

@api_bp.route('/contributors/<int:contributor_id>', methods=['GET'])
def get_contributor(contributor_id):
    """Get a specific contributor"""
    contributor = Contributor.query.get_or_404(contributor_id)
    return jsonify(contributor.to_dict())

@api_bp.route('/contributors', methods=['POST'])
def create_contributor():
    """Create a new contributor"""
    data = request.json
    contributor = Contributor(
        name=data.get('name'),
        role=data.get('role'),
        email=data.get('email'),
        bio=data.get('bio'),
        image_url=data.get('image_url')
    )
    db.session.add(contributor)
    db.session.commit()
    return jsonify(contributor.to_dict()), 201

@api_bp.route('/contributors/<int:contributor_id>', methods=['PUT'])
def update_contributor(contributor_id):
    """Update a contributor"""
    contributor = Contributor.query.get_or_404(contributor_id)
    data = request.json
    contributor.name = data.get('name', contributor.name)
    contributor.role = data.get('role', contributor.role)
    contributor.email = data.get('email', contributor.email)
    contributor.bio = data.get('bio', contributor.bio)
    contributor.image_url = data.get('image_url', contributor.image_url)
    db.session.commit()
    return jsonify(contributor.to_dict())

@api_bp.route('/contributors/<int:contributor_id>', methods=['DELETE'])
def delete_contributor(contributor_id):
    """Delete a contributor"""
    contributor = Contributor.query.get_or_404(contributor_id)
    db.session.delete(contributor)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

# ==================== CERTIFICATIONS ====================

@api_bp.route('/certifications', methods=['GET'])
def get_certifications():
    """Get all certifications"""
    certifications = Certification.query.all()
    return jsonify([c.to_dict() for c in certifications])

# ==================== SYNERGIES ====================

@api_bp.route('/synergies', methods=['GET'])
def get_synergies():
    """Get all synergies"""
    synergies = Synergy.query.all()
    return jsonify([s.to_dict() for s in synergies])

