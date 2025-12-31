"""
Terms & Conditions API
"""
import eel
import json
from pathlib import Path
from app.database.connection import SessionLocal
from sqlalchemy import text

# Default dropdown options
DEFAULT_OPTIONS = {
    'payment': [
        '100% against Proforma Invoice',
        '50% Advance, 50% against Delivery',
        '30 Days Credit',
        '60 Days Credit'
    ],
    'priceBasis': [
        'Ex-Works Chakan, Pune Basis',
        'FOR Destination',
        'CIF',
        'FOB'
    ],
    'pfCharges': [
        '2% Extra on the Basic Price',
        '3% Extra on the Basic Price',
        'Included',
        'As Actual'
    ],
    'insurance': [
        'Shall be borne by you',
        'Included in price',
        'To be arranged by buyer'
    ],
    'deliveryPeriod': [
        '8 weeks from date of technically and commercially clear PO',
        '6 weeks from date of technically and commercially clear PO',
        '10 weeks from date of technically and commercially clear PO',
        '12 weeks from date of technically and commercially clear PO'
    ]
}

def get_terms_options_file():
    """Get path to terms options JSON file"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    return data_dir / 'terms_options.json'

def load_dropdown_options():
    """Load dropdown options from file or use defaults"""
    options_file = get_terms_options_file()
    if options_file.exists():
        with open(options_file, 'r') as f:
            return json.load(f)
    return DEFAULT_OPTIONS.copy()

def save_dropdown_options(options):
    """Save dropdown options to file"""
    options_file = get_terms_options_file()
    with open(options_file, 'w') as f:
        json.dump(options, f, indent=2)

@eel.expose
def get_terms_dropdown_options():
    """Get all dropdown options"""
    try:
        options = load_dropdown_options()
        return {'success': True, 'data': options}
    except Exception as e:
        return {'success': False, 'message': str(e)}

@eel.expose
def add_terms_dropdown_option(field, value):
    """Add new option to dropdown"""
    try:
        options = load_dropdown_options()
        
        if field not in options:
            return {'success': False, 'message': 'Invalid field'}
        
        if value not in options[field]:
            options[field].append(value)
            save_dropdown_options(options)
        
        return {'success': True, 'data': options}
    except Exception as e:
        return {'success': False, 'message': str(e)}

@eel.expose
def save_custom_terms(quotation_number, terms_text):
    """Save custom terms for a quotation"""
    db = SessionLocal()
    try:
        # Check if commercial quote exists
        result = db.execute(text("""
            SELECT id FROM commercial_quotations
            WHERE quotation_number = :quotation_number
        """), {'quotation_number': quotation_number}).fetchone()
        
        if result:
            # Update existing
            db.execute(text("""
                UPDATE commercial_quotations 
                SET terms = :terms, updated_at = CURRENT_TIMESTAMP
                WHERE quotation_number = :quotation_number
            """), {'terms': terms_text, 'quotation_number': quotation_number})
        else:
            # Create new entry with just terms
            db.execute(text("""
                INSERT INTO commercial_quotations (quotation_number, terms, created_at, updated_at)
                VALUES (:quotation_number, :terms, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """), {'quotation_number': quotation_number, 'terms': terms_text})
        
        db.commit()
        return {'success': True, 'message': 'Terms saved successfully'}
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': str(e)}
    finally:
        db.close()

@eel.expose
def get_quote_terms(quotation_number):
    """Get saved terms for a quotation"""
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT terms FROM commercial_quotations
            WHERE quotation_number = :quotation_number
        """), {'quotation_number': quotation_number}).fetchone()
        
        if result and result[0]:
            return {'success': True, 'data': result[0]}
        return {'success': True, 'data': None}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    finally:
        db.close()

@eel.expose
def save_general_conditions(quotation_number, conditions_text):
    """Save general conditions for a quotation"""
    db = SessionLocal()
    try:
        # Check if commercial quote exists
        result = db.execute(text("""
            SELECT id FROM commercial_quotations
            WHERE quotation_number = :quotation_number
        """), {'quotation_number': quotation_number}).fetchone()
        
        if result:
            # Update existing
            db.execute(text("""
                UPDATE commercial_quotations 
                SET general_conditions = :conditions, updated_at = CURRENT_TIMESTAMP
                WHERE quotation_number = :quotation_number
            """), {'conditions': conditions_text, 'quotation_number': quotation_number})
        else:
            # Create new entry
            db.execute(text("""
                INSERT INTO commercial_quotations (quotation_number, general_conditions, created_at, updated_at)
                VALUES (:quotation_number, :conditions, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """), {'quotation_number': quotation_number, 'conditions': conditions_text})
        
        db.commit()
        return {'success': True, 'message': 'General conditions saved successfully'}
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': str(e)}
    finally:
        db.close()

@eel.expose
def get_general_conditions(quotation_number):
    """Get saved general conditions for a quotation"""
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT general_conditions FROM commercial_quotations
            WHERE quotation_number = :quotation_number
        """), {'quotation_number': quotation_number}).fetchone()
        
        if result and result[0]:
            return {'success': True, 'data': result[0]}
        return {'success': True, 'data': None}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    finally:
        db.close()