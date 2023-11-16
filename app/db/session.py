from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .base import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
