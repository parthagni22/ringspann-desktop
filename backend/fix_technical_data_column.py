# backend/fix_technical_data_column.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        print("Checking technical_quotations table...")
        
        result = db.execute(text("PRAGMA table_info(technical_quotations)")).fetchall()
        columns = [col[1] for col in result]
        print(f"Current columns: {columns}")
        
        if 'technical_data' not in columns:
            print("Adding technical_data column...")
            db.execute(text("ALTER TABLE technical_quotations ADD COLUMN technical_data TEXT"))
            db.commit()
            print("✓ Added technical_data column")
        else:
            print("• technical_data column already exists")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()