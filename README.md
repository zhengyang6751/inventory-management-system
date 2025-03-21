# Inventory Management System

A comprehensive inventory management solution for small retail stores, built with modern full-stack architecture.

## Tech Stack

### Frontend

- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- React Query for state management
- Axios for API communication

### Backend

- FastAPI (Python 3.8+)
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Alembic for migrations

## Features

- User Authentication System
- Real-time Stock Level Tracking and Alerts
- Sales Transaction Management
- Supplier Information Management
- Returns Processing
- Automated Reporting
- Data Backup System
- Barcode Scanning Support

## Project Structure

```
inventory_management/
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── utils/         # Utility functions
│   │   ├── hooks/         # Custom React hooks
│   │   └── store/         # State management
│   ├── public/            # Static assets
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configurations
│   │   ├── db/           # Database setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── tests/
│   └── requirements.txt
│
└── docker/                # Docker configuration
    ├── docker-compose.yml
    ├── Dockerfile.frontend
    └── Dockerfile.backend
```

## Getting Started

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Setup

```bash
docker-compose up -d
```

## API Documentation

Once the backend is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Frontend Development

```bash
cd frontend
npm run dev
```

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload
```

## Testing

### Frontend Tests

```bash
cd frontend
npm test
```

### Backend Tests

```bash
cd backend
pytest
```

## Deployment

The application can be deployed using Docker:

```bash
docker-compose -f docker/docker-compose.yml up -d
```

## License

MIT License
