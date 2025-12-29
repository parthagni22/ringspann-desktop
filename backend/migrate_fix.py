"""Add customer_id foreign key to projects table"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        # Check and add customer_id column
        result = db.execute(text("PRAGMA table_info(projects)")).fetchall()
        columns = [col[1] for col in result]
        
        if 'customer_id' not in columns:
            db.execute(text("ALTER TABLE projects ADD COLUMN customer_id INTEGER"))
            print("✓ Added customer_id column")
        else:
            print("• customer_id column already exists")
        
        if 'requirements_data' not in columns:
            db.execute(text("ALTER TABLE projects ADD COLUMN requirements_data TEXT"))
            print("✓ Added requirements_data column")
        else:
            print("• requirements_data column already exists")
        
        db.commit()
        print("✓ Migration completed successfully")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()