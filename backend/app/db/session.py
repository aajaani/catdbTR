import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# CONNECT SQLALCHEMY TO THE DATABASE
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("CATDB_DATABASE_URL")
    or "postgresql+psycopg://user:password@localhost:5432/catdb"
)
engine = create_engine(DATABASE_URL)

# each query creates a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
