"""
Database Setup Script
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database.connection import init_database

if __name__ == '__main__':
    print("Initializing database...")
    init_database()
    print("✅ Database initialized successfully!")
