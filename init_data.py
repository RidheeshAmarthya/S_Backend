from models import db, FoundationalPrinciple, CorePillar, SustainabilityStrategy, Project, Contributor, Certification, Synergy

def init_sample_data():
    """Initialize database with sample data from Excel structure"""
    
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # 1. Create 7 Foundational Principles (fixed)
    principles_data = [
        {"name": "Environmental Stewardship", "description": "Commitment to protecting and enhancing the natural environment"},
        {"name": "Social Responsibility", "description": "Creating positive social impact for communities and stakeholders"},
        {"name": "Economic Viability", "description": "Ensuring long-term economic sustainability and value creation"},
        {"name": "Resource Efficiency", "description": "Optimizing use of resources including energy, water, and materials"},
        {"name": "Health & Wellbeing", "description": "Promoting health and wellbeing for occupants and communities"},
        {"name": "Resilience & Adaptation", "description": "Building resilience to climate change and future challenges"},
        {"name": "Innovation & Technology", "description": "Leveraging innovation and technology for sustainable solutions"}
    ]
    
    principles = []
    for p_data in principles_data:
        principle = FoundationalPrinciple(**p_data)
        db.session.add(principle)
        principles.append(principle)
    
    db.session.commit()
    
    # 2. Create Green Building Certifications
    certifications_data = [
        {"name": "SBTi"},
        {"name": "GHG Protocol"},
        {"name": "UN SDG"},
        {"name": "BREEAM"},
        {"name": "LEED"},
        {"name": "WELL"},
        {"name": "National Priority"}
    ]
    
    certifications = []
    for c_data in certifications_data:
        cert = Certification(**c_data)
        db.session.add(cert)
        certifications.append(cert)
    
    db.session.commit()
    
    # 3. Create Synergy Categories
    synergies_data = [
        {"name": "Site & Ecology"},
        {"name": "Energy Efficiency"},
        {"name": "Water Conservation"},
        {"name": "Sustainable Materials"},
        {"name": "Indoor Wellbeing"},
        {"name": "Waste Management"},
        {"name": "Lifecycle Value"}
    ]
    
    synergies = []
    for s_data in synergies_data:
        synergy = Synergy(**s_data)
        db.session.add(synergy)
        synergies.append(synergy)
    
    db.session.commit()
    
    # 4. Create sample Core Pillars (under first principle)
    if principles:
        core_pillars_data = [
            {
                "name": "Renewable Energy Integration",
                "description": "Incorporating renewable energy sources",
                "text_content": "Integrating solar, wind, and other renewable energy technologies",
                "author": "Admin",
                "foundational_principle": principles[0],  # Environmental Stewardship
                "certifications": [certifications[0], certifications[1]]  # SBTi, GHG Protocol
            },
            {
                "name": "Community Engagement",
                "description": "Engaging with local communities",
                "text_content": "Building strong relationships with local stakeholders",
                "author": "Admin",
                "foundational_principle": principles[1],  # Social Responsibility
                "certifications": [certifications[2]]  # UN SDG
            },
            {
                "name": "Lifecycle Cost Analysis",
                "description": "Evaluating total cost of ownership",
                "text_content": "Considering long-term economic impacts",
                "author": "Admin",
                "foundational_principle": principles[2],  # Economic Viability
                "certifications": []
            }
        ]
        
        core_pillars = []
        for cp_data in core_pillars_data:
            certs = cp_data.pop('certifications', [])
            fp = cp_data.pop('foundational_principle')
            cp_data['foundational_principle_id'] = fp.id
            
            cp = CorePillar(**cp_data)
            cp.certifications = certs
            db.session.add(cp)
            core_pillars.append(cp)
        
        db.session.commit()
        
        # 5. Create sample Sustainability Strategies
        if core_pillars:
            strategies_data = [
                {
                    "name": "Solar Panel Installation",
                    "description": "Install rooftop solar panels",
                    "text_content": "Photovoltaic panels for renewable electricity generation",
                    "author": "Admin",
                    "cost": "High",
                    "performance_contribution": "Exemplary",
                    "core_pillar": core_pillars[0],
                    "synergies": [synergies[1], synergies[2]]  # Energy Efficiency, Water Conservation
                },
                {
                    "name": "Energy Efficient HVAC",
                    "description": "High-efficiency heating and cooling systems",
                    "text_content": "Modern HVAC systems with high SEER ratings",
                    "author": "Admin",
                    "cost": "Moderate",
                    "performance_contribution": "High",
                    "core_pillar": core_pillars[0],
                    "synergies": [synergies[1], synergies[4]]  # Energy Efficiency, Indoor Wellbeing
                }
            ]
            
            for s_data in strategies_data:
                syns = s_data.pop('synergies', [])
                cp = s_data.pop('core_pillar')
                s_data['core_pillar_id'] = cp.id
                
                strategy = SustainabilityStrategy(**s_data)
                strategy.synergies = syns
                db.session.add(strategy)
            
            db.session.commit()
    
    # 6. Create sample Projects
    projects_data = [
        {
            "project_name": "Green Office Tower",
            "project_size": 50000.0,
            "project_address": "123 Sustainable St, Green City",
            "construction_type": "New Construction",
            "project_type": "Office",
            "design_stage": "Technical Design"
        },
        {
            "project_name": "Eco Residential Complex",
            "project_size": 25000.0,
            "project_address": "456 Eco Avenue, Clean Town",
            "construction_type": "New Construction",
            "project_type": "Resi - Apartment Building",
            "design_stage": "Concept Design"
        }
    ]
    
    for p_data in projects_data:
        project = Project(**p_data)
        db.session.add(project)
    
    db.session.commit()
    
    # 7. Create sample Contributors
    contributors_data = [
        {
            "name": "Jane Smith",
            "role": "Sustainability Consultant",
            "email": "jane.smith@example.com",
            "bio": "Expert in green building design with 15 years of experience"
        },
        {
            "name": "John Doe",
            "role": "Environmental Engineer",
            "email": "john.doe@example.com",
            "bio": "Specialized in renewable energy systems and efficiency"
        }
    ]
    
    for c_data in contributors_data:
        contributor = Contributor(**c_data)
        db.session.add(contributor)
    
    db.session.commit()
    
    print("Database initialized with sample data!")
    print(f"- {FoundationalPrinciple.query.count()} Foundational Principles")
    print(f"- {CorePillar.query.count()} Core Pillars")
    print(f"- {SustainabilityStrategy.query.count()} Sustainability Strategies")
    print(f"- {Project.query.count()} Projects")
    print(f"- {Contributor.query.count()} Contributors")
    print(f"- {Certification.query.count()} Certifications")
    print(f"- {Synergy.query.count()} Synergies")

