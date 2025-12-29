"""
Database Setup Script - FIXED
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Now import will work
from app.database.connection import init_database

if __name__ == '__main__':
    print("Initializing database...")
    init_database()
    print("✅ Database initialized successfully!")