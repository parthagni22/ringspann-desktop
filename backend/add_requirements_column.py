"""
Add requirements_data column to projects table
"""
from app.database.connection import SessionLocal, engine
from sqlalchemy import Column, Text, text

def migrate():
    """Add requirements_data column"""
    db = SessionLocal()
    try:
        # Add column if it doesn't exist
        db.execute(text("""
            ALTER TABLE projects 
            ADD COLUMN IF NOT EXISTS requirements_data TEXT
        """))
        db.commit()
        print("✓ Added requirements_data column to projects table")
    except Exception as e:
        print(f"Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    migrate()