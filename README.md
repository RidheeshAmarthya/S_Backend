# Sustainability Backend System

A Flask-based backend system with REST API and Admin UI for managing sustainability data hierarchy.

## Features

- **REST API**: Full CRUD endpoints for all entities
- **Admin UI**: Web-based interface for viewing and managing data
- **SQL Database**: SQLite database with relational structure
- **Image Uploads**: Support for image uploads for Core Pillars and Strategies
- **Hierarchical Data**: Three-layer structure (Principles → Pillars → Strategies)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the admin UI at: `http://localhost:5003`
4. API endpoints are available at: `http://localhost:5003/api`

## Database Structure

### Foundational Principles (Layer 1)
- Fixed 7 principles (cannot be deleted)
- Always the same 7 items

### Core Pillars (Layer 2)
- Variable: Can add more
- Belongs to a Foundational Principle
- Supports image uploads
- Can have multiple Green Building Certifications

### Sustainability Strategies (Layer 3)
- Variable: Can add more
- Belongs to a Core Pillar
- Supports image uploads
- Has mandatory Cost and Performance Contribution
- Can have multiple Synergies

### Projects
- Project portfolio entries with construction details

### Contributors
- Contributor information for the contributors page

## API Endpoints

### Foundational Principles
- `GET /api/foundational-principles` - List all
- `GET /api/foundational-principles/<id>` - Get one
- `POST /api/foundational-principles` - Create
- `PUT /api/foundational-principles/<id>` - Update
- `DELETE /api/foundational-principles/<id>` - Delete

### Core Pillars
- `GET /api/core-pillars` - List all (optional: `?principle_id=1`)
- `GET /api/core-pillars/<id>` - Get one
- `POST /api/core-pillars` - Create
- `PUT /api/core-pillars/<id>` - Update
- `DELETE /api/core-pillars/<id>` - Delete
- `POST /api/core-pillars/<id>/upload-image` - Upload image

### Sustainability Strategies
- `GET /api/sustainability-strategies` - List all (optional: `?pillar_id=1`)
- `GET /api/sustainability-strategies/<id>` - Get one
- `POST /api/sustainability-strategies` - Create
- `PUT /api/sustainability-strategies/<id>` - Update
- `DELETE /api/sustainability-strategies/<id>` - Delete
- `POST /api/sustainability-strategies/<id>/upload-image` - Upload image

### Projects
- `GET /api/projects` - List all
- `GET /api/projects/<id>` - Get one
- `POST /api/projects` - Create
- `PUT /api/projects/<id>` - Update
- `DELETE /api/projects/<id>` - Delete

### Contributors
- `GET /api/contributors` - List all
- `GET /api/contributors/<id>` - Get one
- `POST /api/contributors` - Create
- `PUT /api/contributors/<id>` - Update
- `DELETE /api/contributors/<id>` - Delete

### Metadata
- `GET /api/certifications` - List all certifications
- `GET /api/synergies` - List all synergies

## Example API Request

```bash
# Get all foundational principles
curl http://localhost:5003/api/foundational-principles

# Create a core pillar
curl -X POST http://localhost:5003/api/core-pillars \
  -H "Content-Type: application/json" \
  -d '{
    "foundational_principle_id": 1,
    "name": "Solar Energy",
    "description": "Solar power integration",
    "author": "John Doe",
    "certification_ids": [1, 2]
  }'
```

## Admin UI

Navigate to `http://localhost:5003/admin` to access the admin interface:
- View all data in tables
- Create new entries via forms
- Delete entries
- Upload images

## Database

The SQLite database file `sustainability_db.sqlite` is created automatically on first run. The database is initialized with sample data including:
- 7 Foundational Principles
- Sample Core Pillars
- Sample Sustainability Strategies
- Sample Projects
- Sample Contributors
- All certifications and synergies

