"""
Database Schema Inspector
Dumps complete schema including tables, columns, types, constraints
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.connection import SessionLocal, engine
from sqlalchemy import inspect, text

def dump_schema():
    inspector = inspect(engine)
    db = SessionLocal()
    
    print("=" * 80)
    print("DATABASE SCHEMA DUMP")
    print("=" * 80)
    
    for table_name in inspector.get_table_names():
        print(f"\n{'='*80}")
        print(f"TABLE: {table_name}")
        print(f"{'='*80}")
        
        # Get columns
        columns = inspector.get_columns(table_name)
        print("\nCOLUMNS:")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col['default']}" if col['default'] else ""
            print(f"  - {col['name']}: {col['type']} {nullable}{default}")
        
        # Get primary keys
        pk = inspector.get_pk_constraint(table_name)
        if pk['constrained_columns']:
            print(f"\nPRIMARY KEY: {', '.join(pk['constrained_columns'])}")
        
        # Get foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            print("\nFOREIGN KEYS:")
            for fk in fks:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        # Get indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\nINDEXES:")
            for idx in indexes:
                unique = "UNIQUE" if idx['unique'] else ""
                print(f"  - {idx['name']}: {idx['column_names']} {unique}")
        
        # Get row count
        try:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            print(f"\nROW COUNT: {result}")
        except:
            pass
    
    db.close()
    
    print("\n" + "=" * 80)
    print("SCHEMA DUMP COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    dump_schema()