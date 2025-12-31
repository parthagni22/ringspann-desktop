"""
Commercial Quote API endpoints
"""
import eel
import json
from app.database.connection import SessionLocal
from app.models.commercial_quotation import CommercialQuotation
from app.models.project import Project

@eel.expose
def save_commercial_quote(project_id: int, quotation_number: str, form_data: dict):
    """Save or update commercial quotation"""
    db = SessionLocal()
    try:
        # Check if quote already exists
        existing = db.query(CommercialQuotation).filter(
            CommercialQuotation.quotation_number == quotation_number
        ).first()
        
        if existing:
            # Update existing
            existing.to = form_data.get('to')
            existing.attn = form_data.get('attn')
            existing.email_to = form_data.get('email_to')
            existing.your_inquiry_ref = form_data.get('your_inquiry_ref')
            existing.pages = form_data.get('pages')
            existing.your_partner = form_data.get('your_partner')
            existing.mobile_no = form_data.get('mobile_no')
            existing.fax_no = form_data.get('fax_no')
            existing.email_partner = form_data.get('email_partner')
            existing.items = json.dumps(form_data.get('items', []))
            
            # Calculate totals
            items = form_data.get('items', [])
            subtotal = sum(item.get('total_price', 0) for item in items)
            existing.subtotal = subtotal
            existing.tax_amount = 0.0  # Add tax calculation if needed
            existing.total_amount = subtotal
            
            db.commit()
            return {"success": True, "message": "Commercial quote updated"}
        else:
            # Create new
            items = form_data.get('items', [])
            subtotal = sum(item.get('total_price', 0) for item in items)
            
            new_quote = CommercialQuotation(
                quotation_number=quotation_number,
                to=form_data.get('to'),
                attn=form_data.get('attn'),
                email_to=form_data.get('email_to'),
                your_inquiry_ref=form_data.get('your_inquiry_ref'),
                pages=form_data.get('pages'),
                your_partner=form_data.get('your_partner'),
                mobile_no=form_data.get('mobile_no'),
                fax_no=form_data.get('fax_no'),
                email_partner=form_data.get('email_partner'),
                items=json.dumps(items),
                subtotal=subtotal,
                tax_amount=0.0,
                total_amount=subtotal
            )
            
            db.add(new_quote)
            db.commit()
            return {"success": True, "message": "Commercial quote created"}
            
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}
    finally:
        db.close()

@eel.expose
def get_commercial_quote(quotation_number: str):
    """Get commercial quotation by quotation number"""
    db = SessionLocal()
    try:
        quote = db.query(CommercialQuotation).filter(
            CommercialQuotation.quotation_number == quotation_number
        ).first()
        
        if not quote:
            return {"success": False, "message": "Quote not found"}
        
        return {
            "success": True,
            "data": {
                "id": quote.id,
                "quotation_number": quote.quotation_number,
                "to": quote.to,
                "attn": quote.attn,
                "email_to": quote.email_to,
                "your_inquiry_ref": quote.your_inquiry_ref,
                "pages": quote.pages,
                "your_partner": quote.your_partner,
                "mobile_no": quote.mobile_no,
                "fax_no": quote.fax_no,
                "email_partner": quote.email_partner,
                "items": json.loads(quote.items or '[]'),
                "subtotal": quote.subtotal,
                "tax_amount": quote.tax_amount,
                "total_amount": quote.total_amount,
                "created_at": quote.created_at.isoformat() if quote.created_at else None
            }
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        db.close()

@eel.expose
def generate_commercial_pdf(quotation_number: str, form_data: dict):
    """Generate PDF for commercial quotation"""
    from app.api.pdf_generator import generate_commercial_pdf as _gen_pdf
    return _gen_pdf(quotation_number, form_data)