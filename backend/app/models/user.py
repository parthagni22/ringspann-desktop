"""
User Model - Updated with Region field
"""
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.models.base import Base, TimestampMixin
import enum

class UserRegion(enum.Enum):
    EAST = "East"
    WEST = "West"
    NORTH = "North"
    SOUTH = "South"

class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)  # email format
    region = Column(Enum(UserRegion), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')  # admin, user
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'region': self.region.value if self.region else None,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }