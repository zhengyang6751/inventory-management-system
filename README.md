# Inventory Management System

A full-stack inventory management system built with FastAPI (Backend) and React (Frontend).

## Features

- User Authentication (Login/Register)
- Product Management
  - Add, Edit, Delete Products
  - Track Stock Levels
  - Barcode Support
  - Category Management
- Supplier Management
  - Add, Edit, Delete Suppliers
  - Track Supplier Information
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

- Python 3.8+
- Node.js 16+
- PostgreSQL

### Backend Setup

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

4. Create a `.env` file in the backend directory with the following content:

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db
   SECRET_KEY=your-secret-key
   ```

5. Run database migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create a `.env` file in the frontend directory:

   ```
   VITE_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Docker Setup

You can also run the entire application using Docker:

1. Make sure Docker and Docker Compose are installed

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

The application will be available at:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Default Admin Account

After setting up, you can log in with the default admin account:

- Email: admin@example.com
- Password: admin

## License

MIT License
