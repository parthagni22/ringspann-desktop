"""
Main Application Entry Point - DESKTOP MODE
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
from app.api import auth_api, customer_api, quotation_api, analytics_api, project_api

# Setup logger
logger = setup_logger()

def initialize_app():
    """Initialize application"""
    logger.info(f"Starting {APP_NAME}")
    
    # Initialize database
    logger.info("Initializing database...")
    init_database()
    logger.info("Database initialized")
    
    logger.info("Application initialized successfully")

def start_app():
    """Start the Eel application in DESKTOP mode"""
    try:
        # Initialize
        initialize_app()
        
        # Initialize Eel with the frontend folder
        eel.init(str(EEL_FOLDER))
        
        logger.info(f"Starting Eel server on port {EEL_PORT}")
        
        # Start Eel in DESKTOP MODE with custom window
        eel.start(
            'index.html',
            size=(1400, 900),           # Window size
            port=EEL_PORT,
            mode='chrome-app',          # Opens as desktop app (not browser)
            host='localhost',
            block=True,
            position=(100, 50),         # Window position on screen
            disable_cache=True,
            cmdline_args=[
                '--disable-http-cache',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-infobars',
                '--window-size=1400,900',
                '--app=http://localhost:' + str(EEL_PORT)
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        
        # Fallback to browser if chrome-app fails
        try:
            logger.info("Falling back to browser mode...")
            eel.start(
                'index.html',
                size=(1400, 900),
                port=EEL_PORT,
                mode='default',
                block=True
            )
        except:
            logger.error("Could not start application in any mode")
            raise

if __name__ == '__main__':
    start_app()