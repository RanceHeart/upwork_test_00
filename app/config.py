import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://user:password@localhost/dbname')
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
ALGORITHM = 'HS256'