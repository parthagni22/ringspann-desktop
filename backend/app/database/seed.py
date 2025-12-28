"""
Database Seeding - Default Data
"""
from app.database.connection import SessionLocal
from app.models.user import User
from app.utils.password import hash_password
from app.utils.logger import setup_logger

logger = setup_logger()

def create_default_admin():
    """Create default admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin exists
        existing_admin = db.query(User).filter(User.username == 'admin').first()
        
        if not existing_admin:
            admin = User(
                username='admin',
                email='admin@ringspann.com',
                password_hash=hash_password('admin123'),
                full_name='Administrator',
                role='admin',
                is_active=True
            )
            
            db.add(admin)
            db.commit()
            
            logger.info("✅ Default admin user created")
            logger.info("   Username: admin")
            logger.info("   Password: admin123")
            logger.info("   ⚠️  Please change password after first login!")
        else:
            logger.info("Admin user already exists")
            
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")
        db.rollback()
    finally:
        db.close()
