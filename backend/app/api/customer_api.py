"""
Customer API
"""
import eel
from app.services.customer_service import CustomerService
from app.utils.logger import setup_logger

logger = setup_logger()
customer_service = CustomerService()

@eel.expose
def get_all_customers():
    """Get all customers"""
    try:
        customers = customer_service.get_all()
        return {'success': True, 'data': customers}
    except Exception as e:
        logger.error(f"Get customers failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def create_customer(data: dict):
    """Create new customer"""
    try:
        customer = customer_service.create(data)
        return {'success': True, 'data': customer}
    except Exception as e:
        logger.error(f"Create customer failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def update_customer(customer_id: int, data: dict):
    """Update customer"""
    try:
        customer = customer_service.update(customer_id, data)
        return {'success': True, 'data': customer}
    except Exception as e:
        logger.error(f"Update customer failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def delete_customer(customer_id: int):
    """Delete customer"""
    try:
        customer_service.delete(customer_id)
        return {'success': True}
    except Exception as e:
        logger.error(f"Delete customer failed: {e}")
        return {'success': False, 'error': str(e)}
