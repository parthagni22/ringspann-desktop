"""
Authentication API - Eel Exposed Functions
"""
import eel
from app.services.auth_service import AuthService
from app.utils.logger import setup_logger

logger = setup_logger()
auth_service = AuthService()

@eel.expose
def register_user(name: str, username: str, region: str, password: str):
    """Register new user"""
    try:
        user = auth_service.register(name, username, region, password)
        return {
            'success': True, 
            'message': 'Registration successful!',
            'data': user
        }
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        return {
            'success': False, 
            'error': str(e)
        }

@eel.expose
def login(username: str, password: str):
    """Login user"""
    try:
        user = auth_service.login(username, password)
        return {
            'success': True,
            'message': 'Login successful!',
            'data': user
        }
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@eel.expose
def logout():
    """Logout user"""
    try:
        auth_service.logout()
        return {
            'success': True,
            'message': 'Logged out successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@eel.expose
def get_current_user():
    """Get current logged-in user"""
    try:
        user = auth_service.get_current_user()
        return {
            'success': True,
            'data': user
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@eel.expose
def check_auth():
    """Check if user is authenticated"""
    try:
        is_auth = auth_service.is_authenticated()
        return {
            'success': True,
            'data': {
                'authenticated': is_auth,
                'user': auth_service.get_current_user() if is_auth else None
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }