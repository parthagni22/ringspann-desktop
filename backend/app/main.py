"""
Main Application Entry Point
Eel + Python Backend
"""
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
    """Initialize application"""
    logger.info(f"Starting {APP_NAME}")
    
    # Initialize database
    logger.info("Initializing database...")
    init_database()
    logger.info("✅ Database initialized")
    
    logger.info("✅ Application initialized successfully")

def start_app():
    """Start the Eel application"""
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
