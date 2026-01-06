# migrate_add_quote_status.py
from app.database.connection import engine
from sqlalchemy import text

def add_quote_status_column():
    """Add quote_status column to projects table"""
    try:
        with engine.connect() as connection:
            # Check if column already exists
            check_query = text("""
                SELECT COUNT(*) 
                FROM pragma_table_info('projects') 
                WHERE name='quote_status';
            """)
            result = connection.execute(check_query)
            exists = result.scalar() > 0
            
            if exists:
                print("✓ Column 'quote_status' already exists!")
                return
            
            # Add the column
            alter_query = text("""
                ALTER TABLE projects 
                ADD COLUMN quote_status VARCHAR(20) DEFAULT 'Budgetary';
            """)
            connection.execute(alter_query)
            connection.commit()
            
            print("✓ Successfully added 'quote_status' column to projects table!")
            print("✓ Default value set to 'Budgetary'")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nIf you see 'duplicate column' error, the column already exists.")

if __name__ == "__main__":
    print("Running database migration...")
    print("Adding 'quote_status' column to projects table...")
    add_quote_status_column()