"""
Fix timestamp columns - add defaults
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal
from sqlalchemy import text

def fix_timestamps():
    db = SessionLocal()
    try:
        print("Fixing timestamp defaults...")
        
        # Recreate projects table with proper defaults
        db.execute(text("""
            CREATE TABLE projects_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quotation_number VARCHAR(100) NOT NULL UNIQUE,
                customer_name VARCHAR(200) NOT NULL,
                customer_id INTEGER,
                status VARCHAR(20) DEFAULT 'draft',
                requirements_data TEXT,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """))
        
        # Copy data if exists
        result = db.execute(text("SELECT COUNT(*) FROM projects")).scalar()
        if result > 0:
            db.execute(text("""
                INSERT INTO projects_temp 
                SELECT * FROM projects
            """))
        
        db.execute(text("DROP TABLE projects"))
        db.execute(text("ALTER TABLE projects_temp RENAME TO projects"))
        
        # Recreate indexes
        db.execute(text("CREATE INDEX ix_projects_customer_name ON projects(customer_name)"))
        db.execute(text("CREATE UNIQUE INDEX ix_projects_quotation_number ON projects(quotation_number)"))
        
        db.commit()
        print("✓ Timestamps fixed with defaults")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Failed: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    fix_timestamps()