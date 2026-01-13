"""
Technical Quotation Model
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class TechnicalQuotation(Base, TimestampMixin):
    __tablename__ = 'technical_quotations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), ForeignKey('projects.quotation_number', ondelete='CASCADE'), nullable=False, index=True)

    # Link to customer requirement
    requirement_id = Column(Integer, nullable=True, index=True)

    # Product information
    part_type = Column(String(100), nullable=False, index=True)
    part_label = Column(String(200))

    # Customer requirements
    customer_requirements = Column(Text)

    # Technical specifications (stored as JSON)
    specifications = Column(JSON)

    # Technical data (JSON string format - used by API)
    technical_data = Column(Text)

    # Additional data
    notes = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="technical_quotations")

    # Constraints
    __table_args__ = (
        UniqueConstraint('quotation_number', 'requirement_id', name='uq_quotation_requirement'),
    )

    def __repr__(self):
        return f"<TechnicalQuotation {self.quotation_number} - {self.part_type}>"
