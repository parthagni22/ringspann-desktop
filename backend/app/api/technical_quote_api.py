"""
Technical Quote API - UPDATED FOR MULTI-PDF GENERATION
"""
import eel
import json
from app.database.connection import SessionLocal
from sqlalchemy import text

@eel.expose
def get_technical_quotes(quotation_number):
    """Get all technical quotes for a quotation"""
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT requirement_id, technical_data
            FROM technical_quotations
            WHERE quotation_number = :quotation_number
        """), {'quotation_number': quotation_number}).fetchall()
        
        quotes = {}
        for row in result:
            quotes[row[0]] = json.loads(row[1]) if row[1] else {}
        
        return {'success': True, 'data': quotes}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    finally:
        db.close()

@eel.expose
def save_technical_quote(quotation_number, requirement_id, quote_data):
    """Save technical quote for a specific requirement"""
    db = SessionLocal()
    try:
        # Check if exists
        result = db.execute(text("""
            SELECT id FROM technical_quotations
            WHERE quotation_number = :quotation_number AND requirement_id = :requirement_id
        """), {'quotation_number': quotation_number, 'requirement_id': requirement_id}).fetchone()
        
        if result:
            # Update
            db.execute(text("""
                UPDATE technical_quotations
                SET technical_data = :data, updated_at = CURRENT_TIMESTAMP
                WHERE quotation_number = :quotation_number AND requirement_id = :requirement_id
            """), {
                'quotation_number': quotation_number,
                'requirement_id': requirement_id,
                'data': json.dumps(quote_data)
            })
        else:
            # Insert - ADD part_type
            db.execute(text("""
                INSERT INTO technical_quotations 
                (quotation_number, requirement_id, part_type, technical_data, created_at, updated_at)
                VALUES (:quotation_number, :requirement_id, :part_type, :data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """), {
                'quotation_number': quotation_number,
                'requirement_id': requirement_id,
                'part_type': requirement_id,
                'data': json.dumps(quote_data)
            })
        
        db.commit()
        return {'success': True, 'message': 'Technical quote saved'}
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': str(e)}
    finally:
        db.close()

# ============================================================
# UPDATED FUNCTION - HANDLES MULTIPLE PDFs
# ============================================================
@eel.expose
def generate_technical_pdf(quotation_number, metadata, requirements, technical_quotes):
    """
    Generate technical PDFs - ONE PDF PER PART TYPE
    
    Returns:
        {
            'success': True,
            'count': 3,  # Number of PDFs generated
            'files': ['/full/path/to/Brake.pdf', '/full/path/to/Backstop.pdf', ...],
            'filenames': ['Technical_Quote_Brake_123.pdf', 'Technical_Quote_Backstop_123.pdf', ...],
            'message': 'Generated 3 technical PDF(s)'
        }
    """
    from pathlib import Path
    from datetime import datetime
    from app.api.technical_pdf_generator import generate_technical_pdf_dispatch
    
    try:
        output_dir = Path("data/quotations/technical")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # CHANGED: Pass output_dir instead of filepath
        # CHANGED: Returns list of files instead of boolean
        generated_files = generate_technical_pdf_dispatch(
            quotation_number, 
            metadata, 
            requirements, 
            technical_quotes, 
            output_dir  # Directory, not filepath
        )
        
        # CHANGED: Check for list of files
        if generated_files and len(generated_files) > 0:
            # Extract just filenames for display
            filenames = [Path(f).name for f in generated_files]
            
            return {
                'success': True,
                'count': len(generated_files),      # NEW: Number of PDFs
                'files': generated_files,            # NEW: Full paths
                'filenames': filenames,              # NEW: Just names
                'message': f'Generated {len(generated_files)} technical PDF(s)'
            }
        else:
            return {'success': False, 'message': 'No requirements to generate PDF'}
            
    except Exception as e:
        import traceback
        return {
            'success': False, 
            'message': str(e),
            'traceback': traceback.format_exc()
        }