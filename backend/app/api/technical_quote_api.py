"""
Technical Quote API
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
            # Insert
            db.execute(text("""
                INSERT INTO technical_quotations (quotation_number, requirement_id, technical_data, created_at, updated_at)
                VALUES (:quotation_number, :requirement_id, :data, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """), {
                'quotation_number': quotation_number,
                'requirement_id': requirement_id,
                'data': json.dumps(quote_data)
            })
        
        db.commit()
        return {'success': True, 'message': 'Technical quote saved'}
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': str(e)}
    finally:
        db.close()

@eel.expose
def generate_technical_pdf(quotation_number, metadata, requirements, technical_quotes):
    """Generate technical PDF"""
    # TODO: Implement PDF generation
    return {'success': True, 'filename': 'technical_quote.pdf', 'filepath': '/path/to/pdf'}