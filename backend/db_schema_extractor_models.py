"""
Database Schema Extractor - Model-Based Version
Extracts schema information directly from SQLAlchemy models
Run this from the backend directory: python db_schema_extractor_models.py
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from sqlalchemy import inspect, MetaData
from app.database.connection import engine, SessionLocal
from app.models import User, Customer, Project, CommercialQuotation, TechnicalQuotation
from datetime import datetime
import json

def extract_model_schema():
    """Extract schema from SQLAlchemy models"""
    
    print("="*80)
    print("DATABASE SCHEMA EXTRACTION (From Models)")
    print("="*80)
    print(f"\n📅 Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get all models
    models = [User, Customer, Project, CommercialQuotation, TechnicalQuotation]
    
    schema_info = {
        'extraction_date': datetime.now().isoformat(),
        'extraction_method': 'SQLAlchemy Models',
        'tables': []
    }
    
    inspector = inspect(engine)
    db = SessionLocal()
    
    for model in models:
        table_name = model.__tablename__
        
        print(f"\n{'='*80}")
        print(f"📋 TABLE: {table_name}")
        print(f"{'='*80}")
        
        table_info = {
            'table_name': table_name,
            'model_class': model.__name__,
            'columns': [],
            'relationships': [],
            'row_count': 0
        }
        
        # Get columns from inspector
        columns = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        pk_columns = pk_constraint.get('constrained_columns', [])
        
        print(f"\n📌 COLUMNS ({len(columns)} total):")
        print("-" * 80)
        print(f"{'Column Name':<30} {'Type':<20} {'Nullable':<10} {'Default':<20} {'PK'}")
        print("-" * 80)
        
        for col in columns:
            col_name = col['name']
            col_type = str(col['type'])
            nullable = "YES" if col['nullable'] else "NO"
            default = str(col.get('default', '')) if col.get('default') else ""
            is_pk = "✓" if col_name in pk_columns else ""
            
            print(f"{col_name:<30} {col_type:<20} {nullable:<10} {default:<20} {is_pk}")
            
            table_info['columns'].append({
                'name': col_name,
                'type': col_type,
                'nullable': col['nullable'],
                'default': default,
                'primary_key': col_name in pk_columns
            })
        
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        if foreign_keys:
            print(f"\n🔗 FOREIGN KEYS ({len(foreign_keys)} total):")
            print("-" * 80)
            for fk in foreign_keys:
                referred_table = fk['referred_table']
                constrained_cols = fk['constrained_columns']
                referred_cols = fk['referred_columns']
                
                for const_col, ref_col in zip(constrained_cols, referred_cols):
                    print(f"  • {const_col} -> {referred_table}.{ref_col}")
                    if fk.get('options'):
                        print(f"    Options: {fk['options']}")
                
                table_info['relationships'].append({
                    'from_columns': constrained_cols,
                    'to_table': referred_table,
                    'to_columns': referred_cols,
                    'options': fk.get('options', {})
                })
        
        # Get row count
        try:
            row_count = db.query(model).count()
            table_info['row_count'] = row_count
            print(f"\n📊 ROW COUNT: {row_count}")
        except Exception as e:
            print(f"\n⚠️ Could not get row count: {e}")
            table_info['row_count'] = 0
        
        # Get sample data
        if row_count > 0:
            try:
                sample_records = db.query(model).limit(3).all()
                print(f"\n💾 SAMPLE DATA (first 3 rows):")
                print("-" * 80)
                
                table_info['sample_data'] = []
                for record in sample_records:
                    record_dict = {}
                    print("\n  Row:")
                    for col in columns:
                        col_name = col['name']
                        value = getattr(record, col_name, None)
                        
                        # Handle enum values
                        if hasattr(value, 'value'):
                            value = value.value
                        
                        # Truncate long values
                        display_value = str(value) if value is not None else "NULL"
                        if len(display_value) > 50:
                            display_value = display_value[:47] + "..."
                        
                        print(f"    {col_name}: {display_value}")
                        record_dict[col_name] = str(value) if value is not None else None
                    
                    table_info['sample_data'].append(record_dict)
            except Exception as e:
                print(f"\n⚠️ Could not fetch sample data: {e}")
        
        # Get indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print(f"\n🔑 INDEXES ({len(indexes)} total):")
            print("-" * 80)
            table_info['indexes'] = []
            for idx in indexes:
                unique_str = "UNIQUE" if idx['unique'] else "INDEX"
                col_names = ', '.join(idx['column_names'])
                print(f"  • {idx['name']} on ({col_names}) [{unique_str}]")
                
                table_info['indexes'].append({
                    'name': idx['name'],
                    'columns': idx['column_names'],
                    'unique': idx['unique']
                })
        
        schema_info['tables'].append(table_info)
    
    db.close()
    
    # Print statistics
    print(f"\n{'='*80}")
    print("📈 DATABASE STATISTICS")
    print(f"{'='*80}")
    
    total_rows = sum(table['row_count'] for table in schema_info['tables'])
    print(f"\n  Total Tables: {len(schema_info['tables'])}")
    print(f"  Total Rows: {total_rows}")
    
    for table in schema_info['tables']:
        print(f"    • {table['table_name']}: {table['row_count']} rows")
    
    # Save to JSON
    output_file = 'database_schema_from_models.json'
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ Schema extraction complete!")
    print(f"📄 Report saved to: {output_file}")
    print(f"{'='*80}\n")
    
    return schema_info


def generate_analytics_guide(schema_info):
    """Generate an analytics development guide"""
    
    guide = []
    
    guide.append("# Analytics Module Development Guide\n\n")
    guide.append("## Available Tables for Analytics\n\n")
    
    for table in schema_info['tables']:
        guide.append(f"### {table['table_name']} ({table['row_count']} rows)\n\n")
        
        # Analytical fields
        analytical_fields = []
        date_fields = []
        categorical_fields = []
        numeric_fields = []
        
        for col in table['columns']:
            col_type = col['type'].upper()
            
            if 'DATE' in col_type or 'TIME' in col_type:
                date_fields.append(col['name'])
            elif 'INT' in col_type or 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
                numeric_fields.append(col['name'])
            elif 'VARCHAR' in col_type or 'TEXT' in col_type or 'ENUM' in col_type:
                categorical_fields.append(col['name'])
        
        if date_fields:
            guide.append(f"**📅 Date/Time Fields:** {', '.join(date_fields)}\n")
        if numeric_fields:
            guide.append(f"**🔢 Numeric Fields:** {', '.join(numeric_fields)}\n")
        if categorical_fields:
            guide.append(f"**📊 Categorical Fields:** {', '.join(categorical_fields)}\n")
        
        guide.append("\n")
        
        # Suggested KPIs
        guide.append("**Suggested KPIs:**\n\n")
        
        if table['table_name'] == 'projects':
            guide.append("- Total Projects Count\n")
            guide.append("- Projects by Status (draft/in_progress/completed/archived)\n")
            guide.append("- Projects by Quote Status (Budgetary/Active/Lost/Won)\n")
            guide.append("- Projects Created per Month/Week\n")
            guide.append("- Projects by Customer\n")
            guide.append("- Average Project Duration\n")
            guide.append("- Win Rate (Won / Total Projects)\n\n")
        
        elif table['table_name'] == 'commercial_quotations':
            guide.append("- Total Quotations Value\n")
            guide.append("- Average Quotation Value\n")
            guide.append("- Quotations by Customer\n")
            guide.append("- Revenue by Month/Quarter\n")
            guide.append("- Top Products by Revenue\n\n")
        
        elif table['table_name'] == 'technical_quotations':
            guide.append("- Quotations by Part Type\n")
            guide.append("- Most Requested Part Types\n")
            guide.append("- Technical Quote Completion Rate\n\n")
        
        elif table['table_name'] == 'customers':
            guide.append("- Total Customers\n")
            guide.append("- New Customers per Month\n")
            guide.append("- Customers by Region/State\n")
            guide.append("- Active vs Inactive Customers\n\n")
        
        elif table['table_name'] == 'users':
            guide.append("- Total Users\n")
            guide.append("- Users by Region\n")
            guide.append("- Active Users\n")
            guide.append("- User Activity Metrics\n\n")
        
        guide.append("---\n\n")
    
    # Write guide
    output_file = 'analytics_development_guide.md'
    with open(output_file, 'w') as f:
        f.writelines(guide)
    
    print(f"📊 Analytics guide saved to: {output_file}\n")


if __name__ == "__main__":
    try:
        # Extract schema
        schema = extract_model_schema()
        
        if schema:
            # Generate analytics guide
            generate_analytics_guide(schema)
            
            print("\n✨ All reports generated successfully!")
            print("\nFiles created:")
            print("  1. database_schema_from_models.json")
            print("  2. analytics_development_guide.md")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()