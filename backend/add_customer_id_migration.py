"""Add customer_id foreign key to projects table"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        # Add customer_id column
        db.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS customer_id INTEGER"))
        
        # Add requirements_data column  
        db.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS requirements_data TEXT"))
        
        db.commit()
        print("✓ Migration completed: Added customer_id and requirements_data columns")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()