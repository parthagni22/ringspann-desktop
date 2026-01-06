"""
Project Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, ForeignKey

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class ProjectStatus(enum.Enum):
    draft = "draft"
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"
    
# ADD NEW ENUM for Quote Status
class QuoteStatus(enum.Enum):
    budgetary = "Budgetary"
    active = "Active"
    lost = "Lost"
    won = "Won"
    
    

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String(100), unique=True, nullable=False, index=True)
    customer_name = Column(String(200), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.draft)
    quote_status = Column(SQLEnum(QuoteStatus), default=QuoteStatus.budgetary, nullable=True)
    requirements_data = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="projects")
    commercial_quotations = relationship("CommercialQuotation", back_populates="project")
    technical_quotations = relationship("TechnicalQuotation", back_populates="project")