# Employee Management REST API

A RESTful Employee Management API developed using
Python, FastAPI, SQLAlchemy, and PostgreSQL.

The application provides endpoints to create, retrieve,
update, and delete employee records.

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Psycopg
- Alembic
- Pydantic
- Uvicorn
- Swagger UI
- Postman

## Features

- Create employee records
- Retrieve all employees
- Retrieve employee by ID
- Update employee details
- Partially update employee details
- Delete employee records
- Email validation
- Input validation using Pydantic
- Database integration using SQLAlchemy
- Database schema management using Alembic
- REST API documentation using Swagger UI

## Project Structure

    Employee-Management-API/
    |
    |-- app/
    |   |-- database/
    |   |-- models/
    |   |-- schemas/
    |   |-- routes/
    |   |-- crud/
    |   |-- main.py
    |
    |-- alembic/
    |   |-- versions/
    |   |-- env.py
    |
    |-- .env.example
    |-- .gitignore
    |-- alembic.ini
    |-- requirements.txt
    |-- run.py
    |-- README.md

## Installation

### 1. Clone the repository

    git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Navigate to the project

    cd Employee-Management-API

### 3. Create a virtual environment

    python -m venv .venv

### 4. Activate the environment

Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

### 5. Install dependencies

    python -m pip install -r requirements.txt

### 6. Configure environment variables

Create a .env file using .env.example.

Add your PostgreSQL connection URL:

    DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/employee_management_db

### 7. Create the PostgreSQL database

Create a database named:

    employee_management_db

### 8. Apply database migrations

    alembic upgrade head

### 9. Start the application

    python run.py

## API Documentation

After starting the application, open:

    http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/employees | Create employee |
| GET | /api/v1/employees | Get all employees |
| GET | /api/v1/employees/{id} | Get employee by ID |
| PUT | /api/v1/employees/{id} | Update employee |
| PATCH | /api/v1/employees/{id} | Partially update employee |
| DELETE | /api/v1/employees/{id} | Delete employee |

## Database

PostgreSQL is used as the primary database.

SQLAlchemy manages database interactions,
while Alembic handles database schema migrations.



## Author

Likhith T N