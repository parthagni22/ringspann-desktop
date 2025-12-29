"""
Authentication Service - FIXED
"""
from app.database.connection import SessionLocal
from app.models.user import User, UserRegion
from app.utils.password import hash_password, verify_password
from app.utils.logger import setup_logger

logger = setup_logger()

class AuthService:
    def __init__(self):
        self.current_user = None
    
    def register(self, name: str, username: str, region: str, password: str):
        """Register new user"""
        db = SessionLocal()
        try:
            # VALIDATE: Email must end with @ringspann.com
            if not username.endswith('@ringspann.com'):
                raise Exception("User ID must end with @ringspann.com")
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                raise Exception("User ID already exists")
            
            # Validate region
            try:
                user_region = UserRegion[region.upper()]
            except KeyError:
                raise Exception(f"Invalid region: {region}")
            
            # Create new user (username is already complete with @ringspann.com)
            new_user = User(
                name=name,
                username=username,  # Use as-is, already has @ringspann.com
                region=user_region,
                password_hash=hash_password(password),
                role='user',
                is_active=True
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"New user registered: {username}")
            
            return new_user.to_dict()
            
        except Exception as e:
            db.rollback()
            logger.error(f"Registration failed: {e}")
            raise
        finally:
            db.close()
    
    def login(self, username: str, password: str):
        """Login user"""
        db = SessionLocal()
        try:
            # Find user
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                raise Exception("Invalid User ID or password")
            
            # Verify password
            if not verify_password(password, user.password_hash):
                raise Exception("Invalid User ID or password")
            
            # Check if active
            if not user.is_active:
                raise Exception("User account is inactive. Please contact administrator.")
            
            # Set current user
            self.current_user = user.to_dict()
            
            logger.info(f"User logged in: {username}")
            
            return self.current_user
            
        finally:
            db.close()
    
    def logout(self):
        """Logout user"""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user['username']}")
        self.current_user = None
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.current_user is not None