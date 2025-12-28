"""
Quotation Service
"""
from app.database.connection import SessionLocal

class QuotationService:
    def create_commercial(self, data: dict):
        """Create commercial quotation"""
        # TODO: Implement
        return {'id': 1, 'quotation_number': 'Q20250001'}
    
    def generate_commercial_pdf(self, quotation_id: int):
        """Generate commercial PDF"""
        # TODO: Implement
        return '/path/to/pdf'
