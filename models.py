from datetime import datetime, UTC, timezone
from zoneinfo import ZoneInfo
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, null, Boolean


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_active = Column(Boolean)

class Notes(Base):
    __tablename__ = 'notes'

    note_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime,default=null, onupdate=datetime.now(timezone.utc))