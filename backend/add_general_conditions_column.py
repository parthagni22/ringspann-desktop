"""
Add general_conditions column to commercial_quotations table
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        print("Adding general_conditions column...")
        
        # Check if column exists
        result = db.execute(text("PRAGMA table_info(commercial_quotations)")).fetchall()
        columns = [col[1] for col in result]
        
        if 'general_conditions' not in columns:
            db.execute(text("ALTER TABLE commercial_quotations ADD COLUMN general_conditions TEXT"))
            print("✓ Added general_conditions column")
        else:
            print("• general_conditions column already exists")
        
        db.commit()
        print("✓ Migration completed successfully")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()