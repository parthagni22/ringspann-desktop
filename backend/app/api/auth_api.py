"""
Authentication API
"""
import eel
from app.services.auth_service import AuthService
from app.utils.logger import setup_logger

logger = setup_logger()
auth_service = AuthService()

@eel.expose
def login(username: str, password: str):
    """Login user"""
    try:
        result = auth_service.login(username, password)
        return {'success': True, 'data': result}
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def logout():
    """Logout user"""
    try:
        auth_service.logout()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def get_current_user():
    """Get current logged-in user"""
    try:
        user = auth_service.get_current_user()
        return {'success': True, 'data': user}
    except Exception as e:
        return {'success': False, 'error': str(e)}
