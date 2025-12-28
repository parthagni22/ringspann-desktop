"""
Commercial Quotation Model
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class CommercialQuotation(Base, TimestampMixin):
    __tablename__ = 'commercial_quotations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), ForeignKey('projects.quotation_number'), nullable=False, index=True)
    
    # Header information
    to = Column(String(200))
    attn = Column(String(100))
    email_to = Column(String(100))
    your_inquiry_ref = Column(String(100))
    pages = Column(Integer, default=1)
    your_partner = Column(String(100))
    mobile_no = Column(String(20))
    fax_no = Column(String(20))
    email_partner = Column(String(100))
    
    # Items (stored as JSON array)
    items = Column(JSON)  # [{description, qty, unit, unit_price, total_price}]
    
    # Terms & Conditions (stored as JSON)
    terms = Column(JSON)
    
    # Total amount
    subtotal = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    
    # Relationships
    project = relationship("Project", back_populates="commercial_quotations")
    
    def __repr__(self):
        return f"<CommercialQuotation {self.quotation_number}>"
