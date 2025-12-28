"""
Analytics API
"""
import eel
from app.services.analytics_service import AnalyticsService
from app.utils.logger import setup_logger

logger = setup_logger()
analytics_service = AnalyticsService()

@eel.expose
def get_overview_analytics():
    """Get overview analytics"""
    try:
        data = analytics_service.get_overview()
        return {'success': True, 'data': data}
    except Exception as e:
        logger.error(f"Get overview analytics failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def get_product_analytics(date_filter='all', customer_filter='All'):
    """Get product analytics"""
    try:
        data = analytics_service.get_product_analytics(date_filter, customer_filter)
        return {'success': True, 'data': data}
    except Exception as e:
        logger.error(f"Get product analytics failed: {e}")
        return {'success': False, 'error': str(e)}
