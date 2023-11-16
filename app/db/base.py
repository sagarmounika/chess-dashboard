from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

encoded_password = "Codetest25%40"
DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost:5432/chess_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine,)

Base = declarative_base()
