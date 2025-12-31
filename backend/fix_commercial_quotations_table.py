"""
Recreate commercial_quotations table with general_conditions and CASCADE delete
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def fix_table():
    db = SessionLocal()
    try:
        print("Fixing commercial_quotations table...")
        
        # Backup existing data
        print("Backing up data...")
        result = db.execute(text("SELECT * FROM commercial_quotations")).fetchall()
        backup_data = [dict(row._mapping) for row in result] if result else []
        print(f"Found {len(backup_data)} records to backup")
        
        # Drop and recreate table
        print("Recreating table...")
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
                inquiry_date DATE,
                quotation_date DATE,
                items TEXT,
                terms TEXT,
                general_conditions TEXT,
                subtotal FLOAT,
                tax_amount FLOAT,
                total_amount FLOAT,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(quotation_number) REFERENCES projects(quotation_number) ON DELETE CASCADE
            )
        """))
        
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_commercial_quotations_quotation_number ON commercial_quotations(quotation_number)"))
        
        # Restore data
        if backup_data:
            print(f"Restoring {len(backup_data)} records...")
            for record in backup_data:
                columns = ', '.join(record.keys())
                placeholders = ', '.join([f':{k}' for k in record.keys()])
                db.execute(text(f"INSERT INTO commercial_quotations ({columns}) VALUES ({placeholders})"), record)
        
        db.commit()
        print("✓ Table fixed with CASCADE delete and general_conditions column")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    fix_table()