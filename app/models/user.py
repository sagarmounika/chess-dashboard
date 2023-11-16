from sqlalchemy import Column, Integer, String,Boolean,DateTime
from app.db.base import Base
import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)
