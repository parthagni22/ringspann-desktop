"""
User Model
"""
from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default='user')  # admin, user
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
