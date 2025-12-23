from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association tables for many-to-many relationships
core_pillar_certifications = db.Table('core_pillar_certifications',
    db.Column('core_pillar_id', db.Integer, db.ForeignKey('core_pillar.id'), primary_key=True),
    db.Column('certification_id', db.Integer, db.ForeignKey('certification.id'), primary_key=True)
)

strategy_synergies = db.Table('strategy_synergies',
    db.Column('sustainability_strategy_id', db.Integer, db.ForeignKey('sustainability_strategy.id'), primary_key=True),
    db.Column('synergy_id', db.Integer, db.ForeignKey('synergy.id'), primary_key=True)
)

class FoundationalPrinciple(db.Model):
    """Layer 1: Fixed 7 principles that cannot be deleted"""
    __tablename__ = 'foundational_principle'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    core_pillars = db.relationship('CorePillar', backref='foundational_principle', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'core_pillars_count': len(self.core_pillars)
        }

class CorePillar(db.Model):
    """Layer 2: Variable core pillars under foundational principles"""
    __tablename__ = 'core_pillar'
    
    id = db.Column(db.Integer, primary_key=True)
    foundational_principle_id = db.Column(db.Integer, db.ForeignKey('foundational_principle.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    text_content = db.Column(db.Text)  # Text & Photos content
    image_url = db.Column(db.String(500))  # Image upload path
    author = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    certifications = db.relationship('Certification', secondary=core_pillar_certifications, lazy='subquery',
                                     backref=db.backref('core_pillars', lazy=True))
    sustainability_strategies = db.relationship('SustainabilityStrategy', backref='core_pillar', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'foundational_principle_id': self.foundational_principle_id,
            'foundational_principle_name': self.foundational_principle.name if self.foundational_principle else None,
            'name': self.name,
            'description': self.description,
            'text_content': self.text_content,
            'image_url': self.image_url,
            'author': self.author,
            'certifications': [c.to_dict() for c in self.certifications],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sustainability_strategies_count': len(self.sustainability_strategies)
        }

class Certification(db.Model):
    """Green Building Certifications (SBTi, GHG Protocol, etc.)"""
    __tablename__ = 'certification'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon_url': self.icon_url
        }

class SustainabilityStrategy(db.Model):
    """Layer 3: Variable sustainability strategies under core pillars"""
    __tablename__ = 'sustainability_strategy'
    
    id = db.Column(db.Integer, primary_key=True)
    core_pillar_id = db.Column(db.Integer, db.ForeignKey('core_pillar.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    text_content = db.Column(db.Text)  # Text & Photos content
    image_url = db.Column(db.String(500))  # Image upload path
    author = db.Column(db.String(200))
    cost = db.Column(db.String(50))  # Innovative, Very Low, Low, Moderate, High
    performance_contribution = db.Column(db.String(50))  # Low, Moderate, High, Exemplary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    synergies = db.relationship('Synergy', secondary=strategy_synergies, lazy='subquery',
                                backref=db.backref('strategies', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'core_pillar_id': self.core_pillar_id,
            'core_pillar_name': self.core_pillar.name if self.core_pillar else None,
            'name': self.name,
            'description': self.description,
            'text_content': self.text_content,
            'image_url': self.image_url,
            'author': self.author,
            'cost': self.cost,
            'performance_contribution': self.performance_contribution,
            'synergies': [s.to_dict() for s in self.synergies],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Synergy(db.Model):
    """Synergy categories (Site & Ecology, Energy Efficiency, etc.)"""
    __tablename__ = 'synergy'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon_url': self.icon_url
        }

class Project(db.Model):
    """Project Portfolio entries"""
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    project_size = db.Column(db.Numeric(15, 2))  # Number
    project_address = db.Column(db.String(500))
    construction_type = db.Column(db.String(100))  # New Construction, Retrofit, etc.
    project_type = db.Column(db.String(100))  # Resi - Detached House, Office, etc.
    design_stage = db.Column(db.String(100))  # Feasibility Study, Concept Design, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'project_size': float(self.project_size) if self.project_size else None,
            'project_address': self.project_address,
            'construction_type': self.construction_type,
            'project_type': self.project_type,
            'design_stage': self.design_stage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Contributor(db.Model):
    """Contributors page entries"""
    __tablename__ = 'contributor'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200))
    email = db.Column(db.String(200))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'email': self.email,
            'bio': self.bio,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

