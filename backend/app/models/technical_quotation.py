"""
Technical Quotation Model
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class TechnicalQuotation(Base, TimestampMixin):
    __tablename__ = 'technical_quotations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), ForeignKey('projects.quotation_number'), nullable=False, index=True)
    
    # Product information
    part_type = Column(String(100), nullable=False, index=True)
    part_label = Column(String(200))
    
    # Customer requirements
    customer_requirements = Column(Text)
    
    # Technical specifications (stored as JSON)
    specifications = Column(JSON)
    
    # Additional data
    notes = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="technical_quotations")
    
    def __repr__(self):
        return f"<TechnicalQuotation {self.quotation_number} - {self.part_type}>"
