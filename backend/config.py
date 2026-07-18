import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# JWT Secret Key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

print("CONFIG FILE LOADED")
print("DB_HOST:", DB_HOST)
print("DB_USER:", DB_USER)
print("DB_PASSWORD:", DB_PASSWORD)
print("DB_NAME:", DB_NAME)




