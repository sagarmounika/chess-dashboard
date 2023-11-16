# app/models/players.py

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Players(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    rating = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    rating_history = relationship("RatingHistory", back_populates="player")

class RatingHistory(Base):
    __tablename__ = "rating_history"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"))

    player = relationship("Players", back_populates="rating_history")
