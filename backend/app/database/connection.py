"""
Database Connection and Session Management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.config import DATABASE_URL, DATABASE_PATH
from app.models.base import Base
from app.utils.logger import setup_logger

logger = setup_logger()

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database - create all tables"""
    try:
        # Import all models to register them
        from app.models import User, Customer, Project, CommercialQuotation, TechnicalQuotation
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database tables created successfully")
        
        # Create default admin user if not exists
        from app.database.seed import create_default_admin
        create_default_admin()
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
