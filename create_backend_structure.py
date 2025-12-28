"""
Backend Structure Creator
Creates complete backend file structure with initial code
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"
SCRIPTS_DIR = BASE_DIR / "scripts"
DOCS_DIR = BASE_DIR / "docs"
DEPLOY_DIR = BASE_DIR / "deploy"

# File structure with content
FILE_STRUCTURE = {
    # ==================== BACKEND ====================
    "backend/app/__init__.py": """\"\"\"
Ringspann Desktop Application
Backend Package Initialization
\"\"\"
__version__ = "1.0.0"
__author__ = "Ringspann Team"
""",

    "backend/app/config.py": """\"\"\"
Application Configuration
\"\"\"
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
PDF_DIR = DATA_DIR / "pdfs"
EXPORT_DIR = DATA_DIR / "exports"
BACKUP_DIR = DATA_DIR / "backups"
LOG_DIR = DATA_DIR / "logs"

# Create directories if they don't exist
for directory in [DATABASE_DIR, PDF_DIR, EXPORT_DIR, BACKUP_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database configuration
DATABASE_PATH = DATABASE_DIR / "ringspann.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Application settings
APP_NAME = "Ringspann Desktop"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Eel configuration
EEL_FOLDER = BASE_DIR / "frontend" / "dist"
EEL_PORT = 8080

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOG_DIR / "app.log"

# PDF settings
PDF_COMMERCIAL_DIR = PDF_DIR / "commercial"
PDF_TECHNICAL_DIR = PDF_DIR / "technical"

# Create PDF subdirectories
PDF_COMMERCIAL_DIR.mkdir(exist_ok=True)
PDF_TECHNICAL_DIR.mkdir(exist_ok=True)

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%B %d, %Y"

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 1000

# Export settings
EXPORT_FORMATS = ['xlsx', 'csv', 'pdf']

print(f"✅ Configuration loaded")
print(f"   Database: {DATABASE_PATH}")
print(f"   Data dir: {DATA_DIR}")
""",

    "backend/app/main.py": """\"\"\"
Main Application Entry Point
Eel + Python Backend
\"\"\"
import eel
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import EEL_FOLDER, EEL_PORT, APP_NAME
from app.database.connection import init_database
from app.utils.logger import setup_logger

# Import API endpoints
from app.api import auth_api, customer_api, quotation_api, analytics_api

# Setup logger
logger = setup_logger()

def initialize_app():
    \"\"\"Initialize application\"\"\"
    logger.info(f"Starting {APP_NAME}")
    
    # Initialize database
    logger.info("Initializing database...")
    init_database()
    logger.info("✅ Database initialized")
    
    logger.info("✅ Application initialized successfully")

def start_app():
    \"\"\"Start the Eel application\"\"\"
    try:
        # Initialize
        initialize_app()
        
        # Initialize Eel with the frontend folder
        eel.init(str(EEL_FOLDER))
        
        logger.info(f"Starting Eel server on port {EEL_PORT}")
        
        # Start Eel
        eel.start(
            'index.html',
            size=(1400, 900),
            port=EEL_PORT,
            mode=None,  # Will try chrome, edge, then default browser
            block=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == '__main__':
    start_app()
""",

    # ==================== MODELS ====================
    "backend/app/models/__init__.py": """\"\"\"
Database Models
\"\"\"
from app.models.base import Base
from app.models.user import User
from app.models.customer import Customer
from app.models.project import Project
from app.models.commercial_quotation import CommercialQuotation
from app.models.technical_quotation import TechnicalQuotation

__all__ = [
    'Base',
    'User',
    'Customer', 
    'Project',
    'CommercialQuotation',
    'TechnicalQuotation'
]
""",

    "backend/app/models/base.py": """\"\"\"
Base Model
\"\"\"
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    \"\"\"Mixin for timestamp fields\"\"\"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
""",

    "backend/app/models/user.py": """\"\"\"
User Model
\"\"\"
from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default='user')  # admin, user
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
""",

    "backend/app/models/customer.py": """\"\"\"
Customer Model
\"\"\"
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Customer(Base, TimestampMixin):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='India')
    gstin = Column(String(15))
    contact_person = Column(String(100))
    notes = Column(Text)
    
    # Relationships
    projects = relationship("Project", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer {self.name}>"
""",

    "backend/app/models/project.py": """\"\"\"
Project Model
\"\"\"
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin
import enum

class ProjectStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Project(Base, TimestampMixin):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer_name = Column(String(200), nullable=False, index=True)  # Denormalized for analytics
    status = Column(Enum(ProjectStatus), default=ProjectStatus.IN_PROGRESS)
    date_created = Column(DateTime, default=datetime.utcnow, index=True)
    created_by = Column(String(100))
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="projects")
    commercial_quotations = relationship("CommercialQuotation", back_populates="project", cascade="all, delete-orphan")
    technical_quotations = relationship("TechnicalQuotation", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.quotation_number}>"
""",

    "backend/app/models/commercial_quotation.py": """\"\"\"
Commercial Quotation Model
\"\"\"
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class CommercialQuotation(Base, TimestampMixin):
    __tablename__ = 'commercial_quotations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), ForeignKey('projects.quotation_number'), nullable=False, index=True)
    
    # Header information
    to = Column(String(200))
    attn = Column(String(100))
    email_to = Column(String(100))
    your_inquiry_ref = Column(String(100))
    pages = Column(Integer, default=1)
    your_partner = Column(String(100))
    mobile_no = Column(String(20))
    fax_no = Column(String(20))
    email_partner = Column(String(100))
    
    # Items (stored as JSON array)
    items = Column(JSON)  # [{description, qty, unit, unit_price, total_price}]
    
    # Terms & Conditions (stored as JSON)
    terms = Column(JSON)
    
    # Total amount
    subtotal = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    
    # Relationships
    project = relationship("Project", back_populates="commercial_quotations")
    
    def __repr__(self):
        return f"<CommercialQuotation {self.quotation_number}>"
""",

    "backend/app/models/technical_quotation.py": """\"\"\"
Technical Quotation Model
\"\"\"
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class TechnicalQuotation(Base, TimestampMixin):
    __tablename__ = 'technical_quotations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_number = Column(String(50), ForeignKey('projects.quotation_number'), nullable=False, index=True)
    
    # Product information
    part_type = Column(String(100), nullable=False, index=True)
    part_label = Column(String(200))
    
    # Customer requirements
    customer_requirements = Column(Text)
    
    # Technical specifications (stored as JSON)
    specifications = Column(JSON)
    
    # Additional data
    notes = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="technical_quotations")
    
    def __repr__(self):
        return f"<TechnicalQuotation {self.quotation_number} - {self.part_type}>"
""",

    # ==================== DATABASE ====================
    "backend/app/database/__init__.py": """\"\"\"
Database Package
\"\"\"
from app.database.connection import engine, SessionLocal, get_db, init_database

__all__ = ['engine', 'SessionLocal', 'get_db', 'init_database']
""",

    "backend/app/database/connection.py": """\"\"\"
Database Connection and Session Management
\"\"\"
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
    \"\"\"Get database session\"\"\"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    \"\"\"Initialize database - create all tables\"\"\"
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
""",

    "backend/app/database/session.py": """\"\"\"
Database Session Utilities
\"\"\"
from contextlib import contextmanager
from app.database.connection import SessionLocal

@contextmanager
def get_session():
    \"\"\"Context manager for database session\"\"\"
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
""",

    "backend/app/database/seed.py": """\"\"\"
Database Seeding - Default Data
\"\"\"
from app.database.connection import SessionLocal
from app.models.user import User
from app.utils.password import hash_password
from app.utils.logger import setup_logger

logger = setup_logger()

def create_default_admin():
    \"\"\"Create default admin user\"\"\"
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
""",

    # ==================== UTILS ====================
    "backend/app/utils/__init__.py": """\"\"\"
Utility Functions
\"\"\"
""",

    "backend/app/utils/logger.py": """\"\"\"
Logging Configuration
\"\"\"
import logging
from logging.handlers import RotatingFileHandler
from app.config import LOG_FILE, LOG_LEVEL
from pathlib import Path

def setup_logger():
    \"\"\"Setup application logger\"\"\"
    
    # Create logger
    logger = logging.getLogger('ringspann')
    logger.setLevel(LOG_LEVEL)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(LOG_LEVEL)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
""",

    "backend/app/utils/password.py": """\"\"\"
Password Hashing Utilities
\"\"\"
import hashlib
import os

def hash_password(password: str) -> str:
    \"\"\"Hash password using SHA-256 with salt\"\"\"
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwd_hash.hex()

def verify_password(password: str, password_hash: str) -> bool:
    \"\"\"Verify password against hash\"\"\"
    salt = bytes.fromhex(password_hash[:64])
    stored_hash = password_hash[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex() == stored_hash
""",

    "backend/app/utils/validators.py": """\"\"\"
Validation Utilities
\"\"\"
import re
from typing import Optional

def validate_email(email: str) -> bool:
    \"\"\"Validate email format\"\"\"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    \"\"\"Validate phone number\"\"\"
    pattern = r'^[+]?[0-9]{10,15}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))

def validate_gstin(gstin: str) -> bool:
    \"\"\"Validate Indian GSTIN\"\"\"
    if not gstin:
        return True  # Optional
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gstin))
""",

    "backend/app/utils/helpers.py": """\"\"\"
Helper Functions
\"\"\"
from datetime import datetime
from typing import Optional

def format_date(date: datetime, format: str = "%Y-%m-%d") -> str:
    \"\"\"Format datetime to string\"\"\"
    if not date:
        return ""
    return date.strftime(format)

def parse_date(date_str: str, format: str = "%Y-%m-%d") -> Optional[datetime]:
    \"\"\"Parse string to datetime\"\"\"
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        return None

def generate_quotation_number() -> str:
    \"\"\"Generate unique quotation number\"\"\"
    from datetime import datetime
    import random
    
    now = datetime.now()
    random_part = random.randint(1000, 9999)
    return f"Q{now.year}{now.month:02d}{now.day:02d}{random_part}"
""",

    "backend/app/utils/constants.py": """\"\"\"
Application Constants
\"\"\"

# User roles
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

# Project statuses
STATUS_IN_PROGRESS = 'in_progress'
STATUS_COMPLETED = 'completed'
STATUS_CANCELLED = 'cancelled'

# Product types
PRODUCT_TYPES = [
    'Brake Quotation',
    'Locking Element for Conveyor',
    'Over Running Clutch',
    'Coupling and Torque Limiter',
    'Backstop Quotation'
]

# Date filters
DATE_FILTER_ALL = 'all'
DATE_FILTER_7_DAYS = 'last_7_days'
DATE_FILTER_30_DAYS = 'last_30_days'
DATE_FILTER_90_DAYS = 'last_90_days'
""",

    # ==================== API ====================
    "backend/app/api/__init__.py": """\"\"\"
API Endpoints (Eel exposed functions)
\"\"\"
""",

    "backend/app/api/auth_api.py": """\"\"\"
Authentication API
\"\"\"
import eel
from app.services.auth_service import AuthService
from app.utils.logger import setup_logger

logger = setup_logger()
auth_service = AuthService()

@eel.expose
def login(username: str, password: str):
    \"\"\"Login user\"\"\"
    try:
        result = auth_service.login(username, password)
        return {'success': True, 'data': result}
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def logout():
    \"\"\"Logout user\"\"\"
    try:
        auth_service.logout()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def get_current_user():
    \"\"\"Get current logged-in user\"\"\"
    try:
        user = auth_service.get_current_user()
        return {'success': True, 'data': user}
    except Exception as e:
        return {'success': False, 'error': str(e)}
""",

    "backend/app/api/customer_api.py": """\"\"\"
Customer API
\"\"\"
import eel
from app.services.customer_service import CustomerService
from app.utils.logger import setup_logger

logger = setup_logger()
customer_service = CustomerService()

@eel.expose
def get_all_customers():
    \"\"\"Get all customers\"\"\"
    try:
        customers = customer_service.get_all()
        return {'success': True, 'data': customers}
    except Exception as e:
        logger.error(f"Get customers failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def create_customer(data: dict):
    \"\"\"Create new customer\"\"\"
    try:
        customer = customer_service.create(data)
        return {'success': True, 'data': customer}
    except Exception as e:
        logger.error(f"Create customer failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def update_customer(customer_id: int, data: dict):
    \"\"\"Update customer\"\"\"
    try:
        customer = customer_service.update(customer_id, data)
        return {'success': True, 'data': customer}
    except Exception as e:
        logger.error(f"Update customer failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def delete_customer(customer_id: int):
    \"\"\"Delete customer\"\"\"
    try:
        customer_service.delete(customer_id)
        return {'success': True}
    except Exception as e:
        logger.error(f"Delete customer failed: {e}")
        return {'success': False, 'error': str(e)}
""",

    "backend/app/api/quotation_api.py": """\"\"\"
Quotation API
\"\"\"
import eel
from app.services.quotation_service import QuotationService
from app.utils.logger import setup_logger

logger = setup_logger()
quotation_service = QuotationService()

@eel.expose
def create_commercial_quotation(data: dict):
    \"\"\"Create commercial quotation\"\"\"
    try:
        result = quotation_service.create_commercial(data)
        return {'success': True, 'data': result}
    except Exception as e:
        logger.error(f"Create commercial quotation failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def generate_commercial_pdf(quotation_id: int):
    \"\"\"Generate commercial PDF\"\"\"
    try:
        pdf_path = quotation_service.generate_commercial_pdf(quotation_id)
        return {'success': True, 'data': {'path': pdf_path}}
    except Exception as e:
        logger.error(f"Generate PDF failed: {e}")
        return {'success': False, 'error': str(e)}
""",

    "backend/app/api/analytics_api.py": """\"\"\"
Analytics API
\"\"\"
import eel
from app.services.analytics_service import AnalyticsService
from app.utils.logger import setup_logger

logger = setup_logger()
analytics_service = AnalyticsService()

@eel.expose
def get_overview_analytics():
    \"\"\"Get overview analytics\"\"\"
    try:
        data = analytics_service.get_overview()
        return {'success': True, 'data': data}
    except Exception as e:
        logger.error(f"Get overview analytics failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def get_product_analytics(date_filter='all', customer_filter='All'):
    \"\"\"Get product analytics\"\"\"
    try:
        data = analytics_service.get_product_analytics(date_filter, customer_filter)
        return {'success': True, 'data': data}
    except Exception as e:
        logger.error(f"Get product analytics failed: {e}")
        return {'success': False, 'error': str(e)}
""",

    # ==================== SERVICES ====================
    "backend/app/services/__init__.py": """\"\"\"
Business Logic Services
\"\"\"
""",

    "backend/app/services/auth_service.py": """\"\"\"
Authentication Service
\"\"\"
from app.database.connection import SessionLocal
from app.models.user import User
from app.utils.password import verify_password

class AuthService:
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str):
        \"\"\"Login user\"\"\"
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
        \"\"\"Logout user\"\"\"
        self.current_user = None
    
    def get_current_user(self):
        \"\"\"Get current user\"\"\"
        return self.current_user
""",

    "backend/app/services/customer_service.py": """\"\"\"
Customer Service
\"\"\"
from app.database.connection import SessionLocal
from app.models.customer import Customer

class CustomerService:
    def get_all(self):
        \"\"\"Get all customers\"\"\"
        db = SessionLocal()
        try:
            customers = db.query(Customer).all()
            return [self._to_dict(c) for c in customers]
        finally:
            db.close()
    
    def create(self, data: dict):
        \"\"\"Create customer\"\"\"
        db = SessionLocal()
        try:
            customer = Customer(**data)
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return self._to_dict(customer)
        finally:
            db.close()
    
    def update(self, customer_id: int, data: dict):
        \"\"\"Update customer\"\"\"
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                raise Exception("Customer not found")
            
            for key, value in data.items():
                setattr(customer, key, value)
            
            db.commit()
            db.refresh(customer)
            return self._to_dict(customer)
        finally:
            db.close()
    
    def delete(self, customer_id: int):
        \"\"\"Delete customer\"\"\"
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                db.delete(customer)
                db.commit()
        finally:
            db.close()
    
    def _to_dict(self, customer):
        \"\"\"Convert customer to dict\"\"\"
        return {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'city': customer.city,
            'state': customer.state,
            'country': customer.country,
            'gstin': customer.gstin,
            'contact_person': customer.contact_person,
            'notes': customer.notes
        }
""",

    "backend/app/services/quotation_service.py": """\"\"\"
Quotation Service
\"\"\"
from app.database.connection import SessionLocal

class QuotationService:
    def create_commercial(self, data: dict):
        \"\"\"Create commercial quotation\"\"\"
        # TODO: Implement
        return {'id': 1, 'quotation_number': 'Q20250001'}
    
    def generate_commercial_pdf(self, quotation_id: int):
        \"\"\"Generate commercial PDF\"\"\"
        # TODO: Implement
        return '/path/to/pdf'
""",

    "backend/app/services/analytics_service.py": """\"\"\"
Analytics Service
\"\"\"
import pandas as pd
from app.database.connection import SessionLocal, engine
from datetime import datetime, timedelta

class AnalyticsService:
    def get_overview(self):
        \"\"\"Get overview analytics\"\"\"
        db = SessionLocal()
        try:
            # Use pandas for easy aggregation
            projects_df = pd.read_sql("SELECT * FROM projects", engine)
            
            if len(projects_df) == 0:
                return {
                    'total_projects': 0,
                    'total_customers': 0,
                    'completion_rate': 0,
                    'active_projects': 0
                }
            
            return {
                'total_projects': len(projects_df),
                'total_customers': projects_df['customer_name'].nunique(),
                'completion_rate': (projects_df['status'] == 'completed').sum() / len(projects_df) * 100,
                'active_projects': (projects_df['status'] == 'in_progress').sum()
            }
        finally:
            db.close()
    
    def get_product_analytics(self, date_filter, customer_filter):
        \"\"\"Get product analytics\"\"\"
        # TODO: Implement with pandas
        return {
            'total_types': 4,
            'products': []
        }
""",

    # ==================== REPOSITORIES ====================
    "backend/app/repositories/__init__.py": """\"\"\"
Data Access Layer
\"\"\"
""",

    # ==================== SCHEMAS ====================
    "backend/app/schemas/__init__.py": """\"\"\"
Pydantic Schemas for Validation
\"\"\"
""",

    # ==================== PDF ====================
    "backend/app/pdf/__init__.py": """\"\"\"
PDF Generation Module
\"\"\"
""",

    # ==================== ANALYTICS ====================
    "backend/app/analytics/__init__.py": """\"\"\"
Analytics Engine
\"\"\"
""",

    # ==================== REQUIREMENTS ====================
    "backend/requirements.txt": """# Core Framework
eel==0.16.0

# Database
sqlalchemy==2.0.23
alembic==1.13.0

# Data Analysis
pandas==2.1.4
numpy==1.26.2
openpyxl==3.1.2

# PDF Generation
reportlab==4.0.7

# Utilities
python-dateutil==2.8.2
python-dotenv==1.0.0

# Testing
pytest==7.4.3
""",

    # ==================== DATA DIRECTORIES ====================
    "data/.gitkeep": "",
    "data/database/.gitkeep": "",
    "data/pdfs/.gitkeep": "",
    "data/pdfs/commercial/.gitkeep": "",
    "data/pdfs/technical/.gitkeep": "",
    "data/exports/.gitkeep": "",
    "data/backups/.gitkeep": "",
    "data/logs/.gitkeep": "",

    # ==================== SCRIPTS ====================
    "scripts/setup_database.py": """\"\"\"
Database Setup Script
\"\"\"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database.connection import init_database

if __name__ == '__main__':
    print("Initializing database...")
    init_database()
    print("✅ Database initialized successfully!")
""",

    # ==================== DOCS ====================
    "docs/README.md": """# Ringspann Desktop - Documentation

## Architecture
- Frontend: React + Tailwind CSS
- Backend: Python + Eel
- Database: SQLite
- PDF: ReportLab
- Analytics: Pandas

## Modules
1. Authentication
2. Customer Management
3. Quotation Management
4. PDF Generation
5. Analytics Dashboard
""",

    # ==================== ROOT FILES ====================
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log*

# Data
data/database/*.db
data/pdfs/
data/exports/
data/logs/
data/backups/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Build
frontend/dist/
*.exe
""",

    "README.md": """# Ringspann Desktop Application

Industrial quotation management system for Ringspann Power Transmission India.

## Features
- Customer Management
- Commercial & Technical Quotations
- PDF Generation
- Analytics Dashboard
- 100% Offline Desktop Application

## Tech Stack
- **Frontend:** React + Tailwind CSS
- **Backend:** Python + Eel
- **Database:** SQLite
- **PDF:** ReportLab
- **Analytics:** Pandas

## Setup

### Backend
```bash
cd backend
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
npm run build
```

### Run
```bash
cd backend
python app/main.py
```

## Development
Module by module development in progress.

## License
Proprietary - Ringspann Power Transmission India Pvt. Ltd.
""",

    ".env.example": """# Environment Configuration
DEBUG=False
LOG_LEVEL=INFO
""",
}

def create_file(filepath: str, content: str):
    """Create a file with given content"""
    full_path = BASE_DIR / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {filepath}")

def main():
    """Create all files"""
    print("="*70)
    print("  RINGSPANN DESKTOP - BACKEND STRUCTURE CREATOR")
    print("="*70)
    print()
    
    total_files = len(FILE_STRUCTURE)
    
    print(f"Creating {total_files} files...\n")
    
    for filepath, content in FILE_STRUCTURE.items():
        create_file(filepath, content)
    
    print()
    print("="*70)
    print("  ✅ BACKEND STRUCTURE CREATED SUCCESSFULLY!")
    print("="*70)
    print()
    print("Next steps:")
    print("1. cd backend")
    print("2. python -m venv venv")
    print("3. venv\\Scripts\\activate  (Windows)")
    print("4. pip install -r requirements.txt")
    print("5. python app/main.py")
    print()
    print("="*70)

if __name__ == '__main__':
    main()
