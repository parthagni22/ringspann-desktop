import eel
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import init_database
from app.utils.logger import setup_logger
from app.api import auth_api, customer_api, quotation_api, analytics_api, project_api, commercial_quote_api, pdf_generator

logger = setup_logger()

def start_app():
    try:
        logger.info("Starting Ringspann Desktop")
        init_database()
        logger.info("Database initialized")
        
        # Get paths
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        frontend_path = os.path.join(os.path.dirname(backend_dir), 'frontend', 'dist')
        
        eel.init(frontend_path)
        logger.info("Starting desktop application on port 8080")
        
        eel.start(
            'index.html',
            mode='chrome-app',
            host='localhost',
            port=8080,
            size=(1400, 900),
            cmdline_args=['--app=http://localhost:8080'],
            block=True
        )
    except Exception as e:
        logger.error(f"Failed to start: {e}")

if __name__ == '__main__':
    start_app()