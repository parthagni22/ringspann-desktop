"""
Fix commercial_quotations table - make items nullable
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def fix_commercial_table():
    db = SessionLocal()
    try:
        print("Fixing commercial_quotations table...")
        
        # Recreate table with proper schema
        db.execute(text("DROP TABLE IF EXISTS commercial_quotations"))
        
        db.execute(text("""
            CREATE TABLE commercial_quotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quotation_number VARCHAR(50) NOT NULL,
                "to" VARCHAR(200),
                attn VARCHAR(100),
                email_to VARCHAR(100),
                your_inquiry_ref VARCHAR(100),
                pages INTEGER,
                your_partner VARCHAR(100),
                mobile_no VARCHAR(20),
                fax_no VARCHAR(20),
                email_partner VARCHAR(100),
                items TEXT,
                terms TEXT,
                subtotal FLOAT,
                tax_amount FLOAT,
                total_amount FLOAT,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(quotation_number) REFERENCES projects(quotation_number)
            )
        """))
        
        db.execute(text("CREATE INDEX ix_commercial_quotations_quotation_number ON commercial_quotations(quotation_number)"))
        
        db.commit()
        print("✓ Table fixed")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Failed: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    fix_commercial_table()