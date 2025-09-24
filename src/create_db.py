from sqlalchemy import create_engine
from src.database import Base, SessionLocal, DATABASE_URL
from dotenv import load_dotenv
import os

from src.models.users import User
from src.models.tag import Tag
from src.models.photo import Photo

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create the SQLAlchemy engine to connect to the database
def create_database_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine) # Generate tables based on SQLAlchemy models
    print("Tables created successfully.")

if __name__ == "__main__":
    create_database_tables()