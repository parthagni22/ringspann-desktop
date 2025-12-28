"""
Customer Model
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Customer(Base, TimestampMixin):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='India')
    gstin = Column(String(15))
    contact_person = Column(String(100))
    notes = Column(Text)
    
    # Relationships
    projects = relationship("Project", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer {self.name}>"
