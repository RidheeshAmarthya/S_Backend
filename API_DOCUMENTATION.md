# API Documentation

## Base URL
`http://localhost:5003/api`

## Foundational Principles

### List All Principles
```
GET /api/foundational-principles
```

Response:
```json
[
  {
    "id": 1,
    "name": "Environmental Stewardship",
    "description": "Commitment to protecting...",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "core_pillars_count": 5
  }
]
```

### Get Single Principle
```
GET /api/foundational-principles/<id>
```

### Create Principle
```
POST /api/foundational-principles
Content-Type: application/json

{
  "name": "Principle Name",
  "description": "Description text"
}
```

## Core Pillars

### List All Core Pillars
```
GET /api/core-pillars
GET /api/core-pillars?principle_id=1  // Filter by principle
```

Response includes:
- Foundational principle name
- Certifications array
- Sustainability strategies count

### Create Core Pillar
```
POST /api/core-pillars
Content-Type: application/json

{
  "foundational_principle_id": 1,
  "name": "Solar Energy",
  "description": "Solar power integration",
  "text_content": "Detailed content with photos",
  "author": "John Doe",
  "image_url": "/uploads/core-pillars/image.jpg",
  "certification_ids": [1, 2, 3]  // Array of certification IDs
}
```

### Upload Image
```
POST /api/core-pillars/<id>/upload-image
Content-Type: multipart/form-data

image: <file>
```

## Sustainability Strategies

### List All Strategies
```
GET /api/sustainability-strategies
GET /api/sustainability-strategies?pillar_id=1  // Filter by pillar
```

### Create Strategy
```
POST /api/sustainability-strategies
Content-Type: application/json

{
  "core_pillar_id": 1,
  "name": "Solar Panel Installation",
  "description": "Install rooftop solar panels",
  "text_content": "Detailed content",
  "author": "Jane Smith",
  "cost": "High",  // Required: Innovative, Very Low, Low, Moderate, High
  "performance_contribution": "Exemplary",  // Required: Low, Moderate, High, Exemplary
  "image_url": "/uploads/strategies/image.jpg",
  "synergy_ids": [1, 2, 3]  // Array of synergy IDs
}
```

## Projects

### List All Projects
```
GET /api/projects
```

### Create Project
```
POST /api/projects
Content-Type: application/json

{
  "project_name": "Green Office Tower",
  "project_size": 50000.0,
  "project_address": "123 Main St",
  "construction_type": "New Construction",
  "project_type": "Office",
  "design_stage": "Technical Design"
}
```

## Contributors

### List All Contributors
```
GET /api/contributors
```

### Create Contributor
```
POST /api/contributors
Content-Type: application/json

{
  "name": "John Doe",
  "role": "Sustainability Consultant",
  "email": "john@example.com",
  "bio": "Expert in green building...",
  "image_url": "/uploads/contributors/image.jpg"
}
```

## Metadata Endpoints

### Get Certifications
```
GET /api/certifications
```

Response:
```json
[
  {"id": 1, "name": "SBTi", "icon_url": null},
  {"id": 2, "name": "GHG Protocol", "icon_url": null}
]
```

### Get Synergies
```
GET /api/synergies
```

Response:
```json
[
  {"id": 1, "name": "Site & Ecology", "icon_url": null},
  {"id": 2, "name": "Energy Efficiency", "icon_url": null}
]
```

## Common Response Formats

### Success Response
- **GET/POST/PUT**: Returns object/array with status 200/201
- **DELETE**: Returns `{"message": "Deleted successfully"}` with status 200

### Error Response
```json
{
  "error": "Error message description"
}
```
Status codes: 400 (Bad Request), 404 (Not Found), 500 (Server Error)

