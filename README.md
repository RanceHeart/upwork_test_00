# FastAPI MVC App

This is a FastAPI MVC (Model-View-Controller) web application template designed to provide a robust and scalable structure for building web APIs. The project includes authentication, user management, and basic CRUD operations for posts, with comprehensive error handling.

## Technologies

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Environment Management**: Pydantic and dotenv
- **Testing**: pytest

# Installation

## Prerequisites
- Python 3.9+
- MySQL

## Setup

### Clone the repository
```bash
git clone https://github.com/your-username/fastapi_mvc_app.git
cd fastapi_mvc_app
```

### Create and activate a virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set up the database
1. Ensure MySQL is running.
2. Create a MySQL database.
3. Create a .env file in the project root directory and add the following environment variables:
```bash
DATABASE_URL=mysql+mysqlconnector://<username>:<password>@localhost/<database_name>
SECRET_KEY=your_secret_key
```

### Run database migrations
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Running Tests
To run the tests, use the following command:
```bash
pytest -v
```

### Start the FastAPI server
```bash
uvicorn app.main:app --reload
```
