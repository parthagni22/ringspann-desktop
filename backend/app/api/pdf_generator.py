"""
Commercial Quotation PDF Generator
"""
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from pathlib import Path
import os

from app.database.connection import SessionLocal
from app.models.commercial_quotation import CommercialQuotation

def generate_commercial_pdf(quotation_number: str, form_data: dict):
    """Generate PDF for commercial quotation"""
    try:
        # Create output directory
        output_dir = Path("data/quotations/commercial")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = f"Commercial_Quote_{quotation_number.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = output_dir / filename
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Logo (if exists)
        logo_path = Path("frontend/public/assets/ringspann_logo2.png")
        if logo_path.exists():
            logo = Image(str(logo_path), width=2*inch, height=0.5*inch)
            story.append(logo)
            story.append(Spacer(1, 12))
        
        # Title
        story.append(Paragraph("RINGSPANN Power Transmission India Pvt. Ltd.", title_style))
        story.append(Paragraph("Commercial Quotation", subtitle_style))
        story.append(Spacer(1, 20))
        
        # Contact Information Table
        contact_data = [
            ['To:', form_data.get('to', ''), 'Page(s):', str(form_data.get('pages', 1))],
            ['Attn.:', form_data.get('attn', ''), 'Your Partner:', form_data.get('your_partner', '')],
            ['E-mail (To):', form_data.get('email_to', ''), 'Mobile No.:', form_data.get('mobile_no', '')],
            ['Your Inquiry Ref.:', form_data.get('your_inquiry_ref', ''), 'Fax No.:', form_data.get('fax_no', '')],
            ['Inquiry Date:', form_data.get('inquiry_date', ''), 'E-mail (Partner):', form_data.get('email_partner', '')],
            ['Quotation No.:', quotation_number, 'Date:', form_data.get('quotation_date', '')]
        ]
        
        contact_table = Table(contact_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2.5*inch])
        contact_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#374151')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(contact_table)
        story.append(Spacer(1, 20))
        
        # Items Table
        items = form_data.get('items', [])
        
        table_data = [['Sr. No', 'Product / Part Type', 'Description', 'Unit Price\n(INR)', 'Unit', 'Total Price\n(INR)']]
        
        subtotal = 0
        for item in items:
            table_data.append([
                str(item.get('sr_no', '')),
                str(item.get('part_type', '')),
                str(item.get('description', '')),
                f"{float(item.get('unit_price', 0)):.2f}",
                str(item.get('unit', 0)),
                f"{float(item.get('total_price', 0)):.2f}"
            ])
            subtotal += float(item.get('total_price', 0))
        
        # Add subtotal row
        table_data.append(['', '', '', '', 'Subtotal:', f"₹{subtotal:.2f}"])
        
        items_table = Table(table_data, colWidths=[0.6*inch, 1.8*inch, 2.5*inch, 1*inch, 0.8*inch, 1.3*inch])
        items_table.setStyle(TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Body style
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('ALIGN', (0, 1), (0, -2), 'CENTER'),
            ('ALIGN', (3, 1), (3, -2), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -2), 'CENTER'),
            ('ALIGN', (5, 1), (5, -2), 'RIGHT'),
            ('VALIGN', (0, 1), (-1, -2), 'MIDDLE'),
            
            # Grid
            ('GRID', (0, 0), (-1, -2), 1, colors.HexColor('#9ca3af')),
            ('BOX', (0, 0), (-1, -2), 2, colors.HexColor('#9ca3af')),
            
            # Subtotal row
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('ALIGN', (4, -1), (4, -1), 'RIGHT'),
            ('ALIGN', (5, -1), (5, -1), 'RIGHT'),
            ('SPAN', (0, -1), (3, -1)),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 30))
        
        # Terms & Conditions
        story.append(Paragraph("<b>Terms & Conditions:</b>", styles['Heading3']))
        story.append(Spacer(1, 10))
        
        terms = [
            "1. Prices are subject to change without notice.",
            "2. Delivery within 4-6 weeks from date of order confirmation.",
            "3. Payment terms: 50% advance, balance before dispatch.",
            "4. All prices are Ex-Works unless specified otherwise.",
            "5. GST as applicable will be charged extra."
        ]
        
        for term in terms:
            story.append(Paragraph(term, styles['Normal']))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER
        )
        
        story.append(Paragraph(
            "Thank you for your inquiry. We look forward to serving you.",
            footer_style
        ))
        
        # Build PDF
        doc.build(story)
        
        return {
            'success': True,
            'filename': filename,
            'filepath': str(filepath.absolute())
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }