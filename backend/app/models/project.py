"""
Project Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin
import enum

class ProjectStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Project(Base, TimestampMixin):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer_name = Column(String(200), nullable=False, index=True)  # Denormalized for analytics
    status = Column(Enum(ProjectStatus), default=ProjectStatus.IN_PROGRESS)
    date_created = Column(DateTime, default=datetime.utcnow, index=True)
    created_by = Column(String(100))
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="projects")
    commercial_quotations = relationship("CommercialQuotation", back_populates="project", cascade="all, delete-orphan")
    technical_quotations = relationship("TechnicalQuotation", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.quotation_number}>"
