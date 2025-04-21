# Inventory Management System

A full-stack inventory management system built with FastAPI (Backend) and React (Frontend).

## Features

- User Authentication (Login/Register)
- Product Management
  - Add, Edit, Delete Products
  - Track Stock Levels
  - Barcode Support
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
  - Customer Management
- Inventory Tracking
  - Stock Level Monitoring
  - Low Stock Alerts
  - Stock Movement History

## Tech Stack

### Backend

- FastAPI (Python)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Alembic (Database Migrations)
- JWT Authentication

### Frontend

- React
- TypeScript
- Tailwind CSS
- React Query
- React Hook Form

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Quick Start with Docker

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd inventory-management-system
   ```

2. Start all services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

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

5. Start the backend server:
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

## API Documentation

The API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
