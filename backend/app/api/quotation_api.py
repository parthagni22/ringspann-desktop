"""
Quotation API
"""
import eel
from app.services.quotation_service import QuotationService
from app.utils.logger import setup_logger

logger = setup_logger()
quotation_service = QuotationService()

@eel.expose
def create_commercial_quotation(data: dict):
    """Create commercial quotation"""
    try:
        result = quotation_service.create_commercial(data)
        return {'success': True, 'data': result}
    except Exception as e:
        logger.error(f"Create commercial quotation failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def generate_commercial_pdf(quotation_id: int):
    """Generate commercial PDF"""
    try:
        pdf_path = quotation_service.generate_commercial_pdf(quotation_id)
        return {'success': True, 'data': {'path': pdf_path}}
    except Exception as e:
        logger.error(f"Generate PDF failed: {e}")
        return {'success': False, 'error': str(e)}
