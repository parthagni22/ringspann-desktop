"""
Authentication Service
"""
from app.database.connection import SessionLocal
from app.models.user import User
from app.utils.password import verify_password

class AuthService:
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str):
        """Login user"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                raise Exception("Invalid username or password")
            
            if not verify_password(password, user.password_hash):
                raise Exception("Invalid username or password")
            
            if not user.is_active:
                raise Exception("User account is inactive")
            
            self.current_user = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
            
            return self.current_user
            
        finally:
            db.close()
    
    def logout(self):
        """Logout user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get current user"""
        return self.current_user
