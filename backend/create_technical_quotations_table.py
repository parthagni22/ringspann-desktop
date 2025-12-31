"""
Create technical_quotations table
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        print("Creating technical_quotations table...")
        
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS technical_quotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quotation_number VARCHAR(50) NOT NULL,
                requirement_id VARCHAR(100) NOT NULL,
                technical_data TEXT,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(quotation_number) REFERENCES projects(quotation_number) ON DELETE CASCADE,
                UNIQUE(quotation_number, requirement_id)
            )
        """))
        
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_technical_quotations_quotation_number ON technical_quotations(quotation_number)"))
        
        db.commit()
        print("✓ technical_quotations table created")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()