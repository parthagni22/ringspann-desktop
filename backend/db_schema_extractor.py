"""
Database Schema Extractor
Extracts complete database schema including tables, columns, relationships, and sample data
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

def extract_complete_schema(db_path=None):
    """Extract complete database schema with all details"""
    
    # Try multiple possible locations
    possible_paths = [
        'data/ringspann.db',
        'backend/data/ringspann.db',
        '../data/ringspann.db',
        '../../data/ringspann.db',
        'D:/Irizpro/ringspann-desktop/backend/data/ringspann.db'
    ]
    
    if db_path:
        possible_paths.insert(0, db_path)
    
    # Find existing database
    actual_db_path = None
    for path in possible_paths:
        if Path(path).exists():
            actual_db_path = path
            break
    
    if not actual_db_path:
        print(f"❌ Database not found in any of these locations:")
        for path in possible_paths:
            print(f"   - {path}")
        print(f"\n💡 Please provide the correct database path as an argument.")
        return None
    
    db_path = actual_db_path
    print(f"✅ Database found at: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    schema_info = {
        'database_path': db_path,
        'extraction_date': datetime.now().isoformat(),
        'tables': []
    }
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print("="*80)
    print("DATABASE SCHEMA EXTRACTION")
    print("="*80)
    print(f"\n📊 Database: {db_path}")
    print(f"📅 Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n🔍 Found {len(tables)} tables\n")
    
    for (table_name,) in tables:
        print(f"\n{'='*80}")
        print(f"📋 TABLE: {table_name}")
        print(f"{'='*80}")
        
        table_info = {
            'table_name': table_name,
            'columns': [],
            'indexes': [],
            'foreign_keys': [],
            'sample_data': [],
            'row_count': 0
        }
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"\n📌 COLUMNS ({len(columns)} total):")
        print("-" * 80)
        print(f"{'Column Name':<30} {'Type':<15} {'Nullable':<10} {'Default':<15} {'PK'}")
        print("-" * 80)
        
        for col in columns:
            cid, name, col_type, not_null, default_val, pk = col
            nullable = "NO" if not_null else "YES"
            pk_mark = "✓" if pk else ""
            default_str = str(default_val) if default_val else ""
            
            print(f"{name:<30} {col_type:<15} {nullable:<10} {default_str:<15} {pk_mark}")
            
            table_info['columns'].append({
                'name': name,
                'type': col_type,
                'nullable': not not_null,
                'default': default_val,
                'primary_key': bool(pk)
            })
        
        # Get indexes
        cursor.execute(f"PRAGMA index_list({table_name});")
        indexes = cursor.fetchall()
        
        if indexes:
            print(f"\n🔑 INDEXES ({len(indexes)} total):")
            print("-" * 80)
            for idx in indexes:
                seq, name, unique, origin, partial = idx
                unique_str = "UNIQUE" if unique else "INDEX"
                print(f"  • {name} ({unique_str})")
                
                table_info['indexes'].append({
                    'name': name,
                    'unique': bool(unique),
                    'origin': origin
                })
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()
        
        if foreign_keys:
            print(f"\n🔗 FOREIGN KEYS ({len(foreign_keys)} total):")
            print("-" * 80)
            for fk in foreign_keys:
                id, seq, ref_table, from_col, to_col, on_update, on_delete, match = fk
                print(f"  • {from_col} -> {ref_table}.{to_col}")
                print(f"    ON DELETE: {on_delete}, ON UPDATE: {on_update}")
                
                table_info['foreign_keys'].append({
                    'from_column': from_col,
                    'to_table': ref_table,
                    'to_column': to_col,
                    'on_delete': on_delete,
                    'on_update': on_update
                })
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        table_info['row_count'] = row_count
        
        print(f"\n📊 ROW COUNT: {row_count}")
        
        # Get sample data (first 3 rows)
        if row_count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            sample_rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            print(f"\n💾 SAMPLE DATA (first 3 rows):")
            print("-" * 80)
            
            for row in sample_rows:
                sample_record = {}
                print("\n  Row:")
                for col_name, value in zip(column_names, row):
                    # Truncate long values
                    display_value = str(value)
                    if len(display_value) > 50:
                        display_value = display_value[:47] + "..."
                    print(f"    {col_name}: {display_value}")
                    sample_record[col_name] = str(value) if value is not None else None
                
                table_info['sample_data'].append(sample_record)
        
        # Get CREATE TABLE statement
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_statement = cursor.fetchone()
        if create_statement:
            table_info['create_statement'] = create_statement[0]
            print(f"\n📝 CREATE STATEMENT:")
            print("-" * 80)
            print(create_statement[0])
        
        schema_info['tables'].append(table_info)
    
    # Get database statistics
    print(f"\n{'='*80}")
    print("📈 DATABASE STATISTICS")
    print(f"{'='*80}")
    
    total_rows = sum(table['row_count'] for table in schema_info['tables'])
    print(f"\n  Total Tables: {len(schema_info['tables'])}")
    print(f"  Total Rows: {total_rows}")
    
    for table in schema_info['tables']:
        print(f"    • {table['table_name']}: {table['row_count']} rows")
    
    conn.close()
    
    # Save to JSON file
    output_file = 'database_schema_report.json'
    with open(output_file, 'w') as f:
        json.dump(schema_info, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ Schema extraction complete!")
    print(f"📄 JSON report saved to: {output_file}")
    print(f"{'='*80}\n")
    
    return schema_info


def generate_markdown_report(schema_info):
    """Generate a formatted markdown report"""
    
    md_content = []
    
    md_content.append("# Database Schema Report\n")
    md_content.append(f"**Database:** `{schema_info['database_path']}`\n")
    md_content.append(f"**Generated:** {schema_info['extraction_date']}\n")
    md_content.append(f"**Total Tables:** {len(schema_info['tables'])}\n\n")
    
    md_content.append("---\n\n")
    
    # Table of Contents
    md_content.append("## Table of Contents\n\n")
    for idx, table in enumerate(schema_info['tables'], 1):
        md_content.append(f"{idx}. [{table['table_name']}](#{table['table_name'].lower()})\n")
    md_content.append("\n---\n\n")
    
    # Detailed table information
    for table in schema_info['tables']:
        md_content.append(f"## {table['table_name']}\n\n")
        md_content.append(f"**Row Count:** {table['row_count']}\n\n")
        
        # Columns
        md_content.append("### Columns\n\n")
        md_content.append("| Column | Type | Nullable | Default | Primary Key |\n")
        md_content.append("|--------|------|----------|---------|-------------|\n")
        
        for col in table['columns']:
            pk_mark = "✓" if col['primary_key'] else ""
            nullable = "YES" if col['nullable'] else "NO"
            default = col['default'] if col['default'] else ""
            md_content.append(f"| {col['name']} | {col['type']} | {nullable} | {default} | {pk_mark} |\n")
        
        md_content.append("\n")
        
        # Foreign Keys
        if table['foreign_keys']:
            md_content.append("### Foreign Keys\n\n")
            for fk in table['foreign_keys']:
                md_content.append(f"- `{fk['from_column']}` → `{fk['to_table']}.{fk['to_column']}`\n")
                md_content.append(f"  - ON DELETE: {fk['on_delete']}\n")
                md_content.append(f"  - ON UPDATE: {fk['on_update']}\n")
            md_content.append("\n")
        
        # Indexes
        if table['indexes']:
            md_content.append("### Indexes\n\n")
            for idx in table['indexes']:
                idx_type = "UNIQUE" if idx['unique'] else "INDEX"
                md_content.append(f"- `{idx['name']}` ({idx_type})\n")
            md_content.append("\n")
        
        # Sample Data
        if table['sample_data']:
            md_content.append("### Sample Data\n\n")
            md_content.append("```json\n")
            md_content.append(json.dumps(table['sample_data'][:2], indent=2))
            md_content.append("\n```\n\n")
        
        md_content.append("---\n\n")
    
    # Write markdown file
    output_file = 'database_schema_report.md'
    with open(output_file, 'w') as f:
        f.writelines(md_content)
    
    print(f"📄 Markdown report saved to: {output_file}\n")


if __name__ == "__main__":
    # Extract schema
    schema = extract_complete_schema('data/ringspann.db')
    
    if schema:
        # Generate markdown report
        generate_markdown_report(schema)
        
        print("\n✨ All reports generated successfully!")
        print("\nFiles created:")
        print("  1. database_schema_report.json (machine-readable)")
        print("  2. database_schema_report.md (human-readable)")