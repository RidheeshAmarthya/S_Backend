from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db, FoundationalPrinciple, CorePillar, SustainabilityStrategy, Project, Contributor, Certification, Synergy
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder=''):
    """Save uploaded file and return the relative URL"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join('uploads', folder, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        return f"/uploads/{folder}/{filename}"
    return None

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    stats = {
        'foundational_principles': FoundationalPrinciple.query.count(),
        'core_pillars': CorePillar.query.count(),
        'sustainability_strategies': SustainabilityStrategy.query.count(),
        'projects': Project.query.count(),
        'contributors': Contributor.query.count()
    }
    return render_template('admin/index.html', stats=stats)

@admin_bp.route('/foundational-principles')
def foundational_principles():
    """View all foundational principles"""
    principles = FoundationalPrinciple.query.all()
    return render_template('admin/foundational_principles.html', principles=principles)

@admin_bp.route('/core-pillars')
def core_pillars():
    """View all core pillars"""
    pillars = CorePillar.query.all()
    principles = FoundationalPrinciple.query.all()
    certifications = Certification.query.all()
    return render_template('admin/core_pillars.html', pillars=pillars, principles=principles, certifications=certifications)

@admin_bp.route('/sustainability-strategies')
def sustainability_strategies():
    """View all sustainability strategies"""
    strategies = SustainabilityStrategy.query.all()
    pillars = CorePillar.query.all()
    synergies = Synergy.query.all()
    return render_template('admin/sustainability_strategies.html', strategies=strategies, pillars=pillars, synergies=synergies)

@admin_bp.route('/projects')
def projects():
    """View all projects"""
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@admin_bp.route('/contributors')
def contributors():
    """View all contributors"""
    contributors = Contributor.query.all()
    return render_template('admin/contributors.html', contributors=contributors)

# CRUD operations via forms
@admin_bp.route('/core-pillars/create', methods=['POST'])
def create_core_pillar():
    """Create core pillar via form"""
    try:
        pillar = CorePillar(
            foundational_principle_id=request.form.get('foundational_principle_id'),
            name=request.form.get('name'),
            description=request.form.get('description'),
            text_content=request.form.get('text_content'),
            author=request.form.get('author')
        )
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            image_url = save_uploaded_file(file, 'core-pillars')
            if image_url:
                pillar.image_url = image_url
        
        # Handle certifications
        certification_ids = request.form.getlist('certification_ids')
        if certification_ids:
            certifications = Certification.query.filter(Certification.id.in_([int(id) for id in certification_ids])).all()
            pillar.certifications = certifications
        
        db.session.add(pillar)
        db.session.commit()
        flash('Core pillar created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating core pillar: {str(e)}', 'error')
    
    return redirect(url_for('admin.core_pillars'))

@admin_bp.route('/core-pillars/<int:pillar_id>/upload-image', methods=['POST'])
def upload_core_pillar_image(pillar_id):
    """Upload image for core pillar"""
    pillar = CorePillar.query.get_or_404(pillar_id)
    if 'image' in request.files:
        file = request.files['image']
        image_url = save_uploaded_file(file, 'core-pillars')
        if image_url:
            pillar.image_url = image_url
            db.session.commit()
            flash('Image uploaded successfully!', 'success')
    return redirect(url_for('admin.core_pillars'))

@admin_bp.route('/core-pillars/<int:pillar_id>/delete', methods=['POST'])
def delete_core_pillar(pillar_id):
    """Delete core pillar"""
    pillar = CorePillar.query.get_or_404(pillar_id)
    db.session.delete(pillar)
    db.session.commit()
    flash('Core pillar deleted successfully!', 'success')
    return redirect(url_for('admin.core_pillars'))

@admin_bp.route('/sustainability-strategies/create', methods=['POST'])
def create_sustainability_strategy():
    """Create sustainability strategy via form"""
    try:
        strategy = SustainabilityStrategy(
            core_pillar_id=request.form.get('core_pillar_id'),
            name=request.form.get('name'),
            description=request.form.get('description'),
            text_content=request.form.get('text_content'),
            author=request.form.get('author'),
            cost=request.form.get('cost'),
            performance_contribution=request.form.get('performance_contribution')
        )
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            image_url = save_uploaded_file(file, 'strategies')
            if image_url:
                strategy.image_url = image_url
        
        # Handle synergies
        synergy_ids = request.form.getlist('synergy_ids')
        if synergy_ids:
            synergies = Synergy.query.filter(Synergy.id.in_([int(id) for id in synergy_ids])).all()
            strategy.synergies = synergies
        
        db.session.add(strategy)
        db.session.commit()
        flash('Sustainability strategy created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating strategy: {str(e)}', 'error')
    
    return redirect(url_for('admin.sustainability_strategies'))

@admin_bp.route('/sustainability-strategies/<int:strategy_id>/delete', methods=['POST'])
def delete_sustainability_strategy(strategy_id):
    """Delete sustainability strategy"""
    strategy = SustainabilityStrategy.query.get_or_404(strategy_id)
    db.session.delete(strategy)
    db.session.commit()
    flash('Sustainability strategy deleted successfully!', 'success')
    return redirect(url_for('admin.sustainability_strategies'))

@admin_bp.route('/projects/create', methods=['POST'])
def create_project():
    """Create project via form"""
    try:
        project = Project(
            project_name=request.form.get('project_name'),
            project_size=request.form.get('project_size') or None,
            project_address=request.form.get('project_address'),
            construction_type=request.form.get('construction_type'),
            project_type=request.form.get('project_type'),
            design_stage=request.form.get('design_stage')
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating project: {str(e)}', 'error')
    
    return redirect(url_for('admin.projects'))

@admin_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

@admin_bp.route('/contributors/create', methods=['POST'])
def create_contributor():
    """Create contributor via form"""
    try:
        contributor = Contributor(
            name=request.form.get('name'),
            role=request.form.get('role'),
            email=request.form.get('email'),
            bio=request.form.get('bio')
        )
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            image_url = save_uploaded_file(file, 'contributors')
            if image_url:
                contributor.image_url = image_url
        
        db.session.add(contributor)
        db.session.commit()
        flash('Contributor created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating contributor: {str(e)}', 'error')
    
    return redirect(url_for('admin.contributors'))

@admin_bp.route('/contributors/<int:contributor_id>/delete', methods=['POST'])
def delete_contributor(contributor_id):
    """Delete contributor"""
    contributor = Contributor.query.get_or_404(contributor_id)
    db.session.delete(contributor)
    db.session.commit()
    flash('Contributor deleted successfully!', 'success')
    return redirect(url_for('admin.contributors'))

