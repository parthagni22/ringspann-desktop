"""
Fix customer_id constraint - make it nullable
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def fix_customer_id():
    db = SessionLocal()
    try:
        print("Fixing customer_id constraint...")
        
        # SQLite doesn't support ALTER COLUMN, so we need to:
        # 1. Create new table with correct schema
        # 2. Copy data
        # 3. Drop old table
        # 4. Rename new table
        
        db.execute(text("""
            CREATE TABLE projects_new (
                id INTEGER PRIMARY KEY,
                quotation_number VARCHAR(50) NOT NULL UNIQUE,
                customer_id INTEGER,
                customer_name VARCHAR(200) NOT NULL,
                status VARCHAR(11),
                date_created DATETIME,
                created_by VARCHAR(100),
                notes TEXT,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                requirements_data TEXT,
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """))
        
        # Copy existing data (if any)
        result = db.execute(text("SELECT COUNT(*) FROM projects")).scalar()
        if result > 0:
            db.execute(text("""
                INSERT INTO projects_new 
                SELECT * FROM projects
            """))
        
        # Drop old table
        db.execute(text("DROP TABLE projects"))
        
        # Rename new table
        db.execute(text("ALTER TABLE projects_new RENAME TO projects"))
        
        # Recreate indexes
        db.execute(text("CREATE INDEX ix_projects_customer_name ON projects(customer_name)"))
        db.execute(text("CREATE INDEX ix_projects_date_created ON projects(date_created)"))
        db.execute(text("CREATE UNIQUE INDEX ix_projects_quotation_number ON projects(quotation_number)"))
        
        db.commit()
        print("✓ customer_id is now nullable")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Migration failed: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    fix_customer_id()