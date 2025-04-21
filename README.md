# Inventory Management System

A full-stack inventory management system built with FastAPI (Backend) and React (Frontend).

## Features

- User Authentication (Login/Register)
- Product Management
  - Add, Edit, Delete Products
  - Track Stock Levels
  - Category Management
- Category Management
  - Add, Edit, Delete Categories
  - Organize Products by Categories
- Supplier Management
  - Add, Edit, Delete Suppliers
  - Track Supplier Information
  - Contact Details Management
- Sales Management
  - Create Sales Records
  - Track Sales History
- Inventory Tracking
  - Stock Level Monitoring
  - Stock Movement History

## Tech Stack

### Backend

- FastAPI (Python)
- Pydantic (Data Validation)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Alembic (Database Migrations)
- JWT Authentication

### Frontend

- React
- TypeScript
- Vite (Build Tool)
- Tailwind CSS
- React Query
- React Hook Form

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Node.js 16+ (for local development)
- Python 3.8+ (for local development)

### Quick Start with Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd inventory-management-system
   ```

2. Copy the example environment file:

   ```bash
   # For backend
   cp backend/.env.example backend/.env
   ```

3. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. Start all services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

5. Wait for the services to start:

   - The database will initialize first
   - The backend will automatically:
     - Create database tables
     - Initialize default data (admin user, categories, etc.)
   - The frontend will start last

6. Access the application:

   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

7. Default Admin Account:
   - Email: admin@example.com
   - Password: admin

### Development Setup

If you want to run the services separately for development:

#### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env.local` file in the backend directory with the following content:

   ```
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=inventory
   SECRET_KEY=your-secret-key
   ```

5. Initialize the database:

   ```bash
   # Create database tables
   alembic upgrade head

   # Initialize initial data
   python -c "from app.db.init_db import init_db; from app.db.session import SessionLocal; init_db(SessionLocal())"
   ```

6. Start the backend server:
   ```bash
   ENV_FILE=.env.local uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

## Troubleshooting

### Common Issues

1. Frontend Build Error: "Failed to resolve import @/lib/axios"

   - Solution: Make sure you've installed the dependencies by running `npm install` in the frontend directory
   - Check that you're using Node.js version 16 or higher

2. Database Connection Error

   - When using Docker: Make sure you're using `docker-compose up --build` to start all services
   - For local development: Ensure PostgreSQL is running and accessible at localhost:5432

3. Backend Startup Error

   - Check that the database is running and accessible
   - Verify that all environment variables are set correctly
   - Make sure all required Python packages are installed

4. Frontend Development Server Issues
   - Clear your browser cache
   - Delete the `node_modules` folder and run `npm install` again
   - Check that you're using the correct Node.js version

### Still Having Issues?

If you're still experiencing problems:

1. Make sure all services are stopped: `docker-compose down`
2. Remove all containers and volumes: `docker-compose down -v`
3. Rebuild all services: `docker-compose up --build`

## API Documentation

The API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
