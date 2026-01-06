# fix_quote_status_values.py
from app.database.connection import engine
from sqlalchemy import text

def fix_quote_status_values():
    """Convert quote_status values to lowercase"""
    try:
        with engine.connect() as connection:
            # Update all existing records to lowercase
            update_query = text("""
                UPDATE projects 
                SET quote_status = LOWER(quote_status)
                WHERE quote_status IS NOT NULL;
            """)
            result = connection.execute(update_query)
            connection.commit()
            
            rows_updated = result.rowcount
            print(f"✓ Successfully updated {rows_updated} rows")
            print("✓ All quote_status values converted to lowercase")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("Fixing quote_status values...")
    fix_quote_status_values()