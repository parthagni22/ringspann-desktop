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

# REMOVED: generate_commercial_pdf - now in commercial_quote_api.py