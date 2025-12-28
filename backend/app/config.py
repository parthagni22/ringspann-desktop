"""
Application Configuration
"""
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
