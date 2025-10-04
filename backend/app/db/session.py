import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ÜHENDAME SQLALCHEMY ANDMEBAASI
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@localhost:5432/catdb")
engine = create_engine(DATABASE_URL)

# iga päring loob uue sessiooni
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()