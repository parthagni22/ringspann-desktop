# backend/fix_technical_quotations_column.py
"""
Fix technical_quotations table - add requirement_id column
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        print("Adding requirement_id column...")
        
        # Check if column exists
        result = db.execute(text("PRAGMA table_info(technical_quotations)")).fetchall()
        columns = [col[1] for col in result]
        
        if 'requirement_id' not in columns:
            db.execute(text("ALTER TABLE technical_quotations ADD COLUMN requirement_id VARCHAR(100)"))
            print("✓ Added requirement_id column")
        else:
            print("• requirement_id column already exists")
        
        db.commit()
        print("✓ Migration completed")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()