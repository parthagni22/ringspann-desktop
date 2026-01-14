import sys
import os

# Set base path
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Add backend to Python path
sys.path.insert(0, os.path.join(base_path, 'backend'))

import eel
from app.database.connection import init_database
from app.utils.logger import setup_logger
from app.api import auth_api, customer_api, quotation_api, analytics_api, project_api, commercial_quote_api, terms_api, technical_quote_api

logger = setup_logger()

def start_app():
    try:
        logger.info("Starting Quotation System")
        init_database()
        logger.info("Database initialized")
        
        # Set frontend path
        if getattr(sys, 'frozen', False):
            frontend_path = os.path.join(base_path, '_internal', 'web')
        else:
            frontend_path = os.path.join(base_path, 'frontend', 'dist')
        
        logger.info(f"Frontend path: {frontend_path}")
        logger.info(f"Path exists: {os.path.exists(frontend_path)}")
        
        if not os.path.exists(frontend_path):
            raise Exception(f"Frontend folder not found at: {frontend_path}")
        
        eel.init(frontend_path)
        eel.start('index.html', mode='chrome', host='localhost', port=8080, size=(1400, 900), block=True)
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    start_app()