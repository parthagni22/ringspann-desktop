"""
Commercial Quotation PDF Generator - Exact Format with Logo and Footer
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from pathlib import Path
from app.database.connection import SessionLocal
from sqlalchemy import text

class FooteredCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_footer(self, page_count):
        page_width = A4[0]
        
        # Company details footer
        self.setFont("Helvetica", 7)
        y_pos = 80
        
        # Left column
        self.drawString(30, y_pos, "RINGSPANN Power Transmission India Pvt. Ltd.")
        self.drawString(30, y_pos-10, "GAT Numbers 679/2/1")
        self.drawString(30, y_pos-20, "Village Kuruli, Taluka Khed, Chakan-Aland Road,")
        self.drawString(30, y_pos-30, "Pune-410501, Maharashtra, INDIA")
        self.drawString(30, y_pos-40, "Phone: +91 2135 677500")
        self.drawString(30, y_pos-50, "Fax: +91 2135 677505")
        self.drawString(30, y_pos-60, "www.ringspann-india.com")
        self.drawString(30, y_pos-70, "info@ringspann-india.com")
        
        # Middle column
        self.drawString(220, y_pos, "VAT No.: 27220915992V")
        self.drawString(220, y_pos-10, "CST No.: 27220915992C")
        self.drawString(220, y_pos-20, "ECC Reg. No.: AAFCR486&REM001")
        self.drawString(220, y_pos-30, "Service Tax No.: AAFCR4868R50001")
        self.drawString(220, y_pos-40, "CIN No.: U74900PN2011FTC140818")
        self.drawString(220, y_pos-50, "GSTIN: 27AAFCR4868R1ZD")
        
        # Right column
        self.drawString(410, y_pos, "U.22.715")
        self.drawString(410, y_pos-10, "Axis Bank - Pune 411014")
        self.drawString(410, y_pos-20, "IFSC Code: UTIB0001032")
        self.drawString(410, y_pos-30, "Swift Code: AXISINSB073")
        self.drawString(410, y_pos-40, "Account No. 910020047693645")

def generate_commercial_pdf(quotation_number: str, form_data: dict):
    """Generate PDF matching exact quotation format"""
    try:
        output_dir = Path("data/quotations/commercial")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"Commercial_Quote_{quotation_number.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = output_dir / filename
        
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=100
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Styles
        company_name_style = ParagraphStyle(
            'CompanyName',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            spaceAfter=0
        )
        
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=15,
            spaceBefore=10
        )
        
        small_bold = ParagraphStyle(
            'SmallBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8
        )
        
        small_text = ParagraphStyle(
            'Small',
            parent=styles['Normal'],
            fontSize=8,
            leading=11
        )
        
        # PAGE 1: Quotation
        
        # Header with logo and company name
        logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
        if not logo_path.exists():
            # Try alternative path
            logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
        
        if logo_path.exists():
            logo = Image(str(logo_path), width=1.8*inch, height=0.47*inch)
            header_table_data = [[
                "RINGSPANN Power Transmission India Pvt. Ltd.",
                logo
            ]]
        else:
            header_table_data = [[
                "RINGSPANN Power Transmission India Pvt. Ltd.",
                ''
            ]]
        
        header_table = Table(header_table_data, colWidths=[5.2*inch, 1.8*inch])
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 16),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 5))
        
        # Title
        story.append(Paragraph("Quotation", title_style))
        
        # Contact table
        contact_data = [
            [Paragraph('<b>To:</b>', small_bold), form_data.get('to', ''), 
             Paragraph('<b>Page(s):</b>', small_bold), str(form_data.get('pages', 1))],
            [Paragraph('<b>Attn.:</b>', small_bold), form_data.get('attn', ''),
             Paragraph('<b>Your Partner:</b>', small_bold), form_data.get('your_partner', '')],
            [Paragraph('<b>E-mail:</b>', small_bold), form_data.get('email_to', ''),
             Paragraph('<b>Mobile No.:</b>', small_bold), form_data.get('mobile_no', '')],
            [Paragraph('<b>Your Inquiry Ref.:</b>', small_bold), form_data.get('your_inquiry_ref', ''),
             Paragraph('<b>Fax No.:</b>', small_bold), form_data.get('fax_no', '')],
            [Paragraph('<b>Quotation No.:</b>', small_bold), quotation_number,
             Paragraph('<b>E-mail:</b>', small_bold), form_data.get('email_partner', '')],
            [Paragraph('<b>Inquiry Date:</b>', small_bold), 
             form_data.get('inquiry_date', datetime.now().strftime('%B %d, %Y')),
             Paragraph('<b>Date:</b>', small_bold), 
             form_data.get('quotation_date', datetime.now().strftime('%B %d, %Y'))]
        ]
        
        contact_table = Table(contact_data, colWidths=[1.2*inch, 2.3*inch, 1.1*inch, 2.4*inch])
        contact_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(contact_table)
        story.append(Spacer(1, 15))
        
        # Greeting
        inquiry_date = form_data.get('inquiry_date', datetime.now().strftime('%B %d, %Y'))
        greeting = f"Dear Sir,<br/>This is with reference to your mail enquiry dated on {inquiry_date} we are pleased to offer as under: -"
        story.append(Paragraph(greeting, small_text))
        story.append(Spacer(1, 10))
        
        # Items table
        items = form_data.get('items', [])
        
        table_data = [[
            Paragraph('<b>Sr. No</b>', small_bold),
            Paragraph('<b>Description</b>', small_bold),
            Paragraph('<b>Unit Price INR</b>', small_bold),
            Paragraph('<b>Unit</b>', small_bold),
            Paragraph('<b>Total Price</b>', small_bold)
        ]]
        
        for item in items:
            desc = f"{item.get('part_type', '')}<br/>{item.get('description', '')}"
            table_data.append([
                str(item.get('sr_no', '')),
                Paragraph(desc, small_text),
                f"{float(item.get('unit_price', 0)):,.2f}",
                str(item.get('unit', 0)),
                f"{float(item.get('total_price', 0)):,.2f}"
            ])
        
        items_table = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 1.2*inch, 0.6*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 15))
        
        # Load custom terms from database or use defaults
        db = SessionLocal()
        custom_terms_text = None
        try:
            result = db.execute(text("""
                SELECT terms FROM commercial_quotations
                WHERE quotation_number = :quotation_number
            """), {'quotation_number': quotation_number}).fetchone()
            if result and result[0]:
                custom_terms_text = result[0]
        except Exception as e:
            print(f"Error loading terms: {e}")
        finally:
            db.close()
        
        # Terms
        story.append(Paragraph("<b>Important Commercial Terms</b>", small_bold))
        story.append(Spacer(1, 6))
        
        if custom_terms_text:
            terms = [line for line in custom_terms_text.split('\n') if line.strip()]
        else:
            terms = [
                "1) Terms of Payment - 100% against Proforma Invoice.",
                "2) Price basis: Ex-Works Chakan, Pune Basis",
                "3) P&F; Charges: 2% Extra on the Basic Price",
                "4) Insurance: Shall be borne by you.",
                "5) Taxes:",
                "a) I-GST is applicable for Out of Maharashtra",
                "b) C-GST & S-GST is applicable within the State of Maharashtra.",
                "c) U-GST is applicable for Union Territory.",
                "6) Delivery Period: 8 weeks from date of technically and commercially clear PO.",
                "7) Warrantee/ Guarantee: 12 months from the date of commissioning or 18 months from the date of Invoice, whichever is earlier."
            ]
        
        for term in terms:
            story.append(Paragraph(term, small_text))
            story.append(Spacer(1, 3))
        
        story.append(Spacer(1, 10))
        story.append(Paragraph("Our enclosed General Conditions of Delivery and Payment are applicable.", small_text))
        story.append(Spacer(1, 10))
        story.append(Paragraph("We are looking forward to your order.", small_text))
        story.append(Spacer(1, 8))
        story.append(Paragraph("Yours sincerely,<br/><b>RINGSPANN Power Transmission India Pvt. Ltd.</b>", small_text))
        story.append(Spacer(1, 15))
        story.append(Paragraph("NAME: _________________________", small_text))
        story.append(Paragraph("DESIGNATION: _________________________", small_text))
        
        # PAGE BREAK
        story.append(PageBreak())
        
        # PAGE 2: General Conditions (same header)
        # Reuse logo path
        if not logo_path.exists():
            logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
            if not logo_path.exists():
                logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
        story.append(header_table)
        story.append(Spacer(1, 5))
        story.append(Paragraph("Quotation", title_style))
        story.append(Paragraph("<b>General Conditions of Delivery and Payment for Customers</b>", small_bold))
        story.append(Spacer(1, 5))
        story.append(Paragraph("The following General Conditions of Delivery and Payment for Customers shall apply to all deliveries of our products, except as modified by express agreement accepted in writing by both parties", small_text))
        story.append(Spacer(1, 10))
        
        # Conditions in 2 columns
        gc_sections = [
            ("1. Offer and Conclusion of Contract", "Only our offers and written confirmations will be decisive with respect to the scope and type of products delivered. The contract shall be deemed to have been concluded when we have accepted the order in writing; up to that time our quotation is without obligation. Measures, weights, illustrations and drawings are without obligation for the models, unless expressly confirmed by us in writing. Manufacturing and detail drawings will be supplied by us only if agreed upon before conclusion of the contract and confirmed by us in writing. An appropriate extra charge will be levied for the supply of such drawings. Where special tools and gauges or clamping devices are necessary in order to carry out a special order, these will be invoiced additionally, but shall remain our property after completion of the order."),
            ("2. Terms of Delivery", "Prices quoted in our offer are EX Works Chakan Basis. All prices are excluding freight and insurance."),
            ("3. Terms of Payment", "The Terms of Payment as applicable is mentioned in our offer. If the terms of payment laid down in the contract are not complied with, interest will be charged at a rate of 8% above the discount rate. In case of complaints with respect to products received, the customer is requested not suspend payment or make any deductions from the invoiced amount, unless liability is admitted by us."),
            ("4. Retention of Title/Conditional Sale", "The products shall remain our property until payment has been made in full."),
            ("5. Delivery", "The Delivery time is mentioned in our offer. The delivery period shall run from the date on which all technical particulars of the models in questions have been clarified and agreement has been reached between the parties with respect to all details of the contract. In case of unforeseeable circumstances which are beyond our control, i.e., force majeure, operating trouble, delayed deliveries by a subcontractor, rejects in our own plant or at a subcontractor's the delivery period shall be reasonably extended. We shall use our best efforts to honour confirmed delivery dates, which are only approximate. However, if in case of confirmed delivery dates there occurs a delay, an appropriate extension of time shall be granted. Claims for damages or penalties are, therefore, excluded unless its discussed in detail during the placement of the order on us."),
            ("6. Packing & Forwarding Charges", "Packing & Forwarding charge @2% shall be applicable on the Basic price of the contract. In case of NIL P & F, then we shall adopt our standard packing method for the dispatch."),
            ("7. Taxes", "GST shall be applicable as per the slab of HSN Code."),
            ("8. Liability for Defects", "Deficiency claims have to be brought forward immediately upon receipt of the shipment. We warrant the quality of our products in such a manner as to replace or repair all components returned to us because they do not meet the specifications or cannot be used because of defects in workmanship. We accept liability only for defects in design or execution which have been caused by us. For defects in material supplied by us we accept liability only insofar as we should have discovered the deficiency in exercising due diligence. If we are responsible for the technical design, we will accept a deficiency claim only in case the customer can prove that our product does not meet the state of art due to our fault. We are not liable for damages due to normal wear and tear or misuse of the products supplied. Any further claims, such as compensation for direct or indirect damages to machinery or cost incurred in dismantling an assembly work, freight charges or penalties for delay etc. are not covered. Where products have been repaired, altered or overhauled without our consent our liability ceases."),
            ("9. Warranty", "Unless otherwise agreed, we warrant the quality of design and manufacture utilizing good raw material for a period of 12 months from the date of commissioning or 18 months from the date of shipment, whichever is earlier, in such a way that we replace or repair free of charge defective components which have been returned to us."),
            ("10. Cancellation of Contract", "The customer may cancel the contract only if, upon a reasonable extension of time we have failed to remedy a deficiency or if, in such case, we are, for whatever reason, unable to undertake necessary corrections or to supply a replacement part. In the event that the contract should be cancelled by the customer without our fault, the customer shall reimburse to us, without delay, the invoice value of such contract after deduction of the direct costs saved by us as a result of the cancellation."),
            ("11. Purchasing Conditions of Customer", "Purchasing conditions of the customer which are not in compliance with these General Conditions of Delivery and Payment, must be accepted by us in writing in order to be binding. The other provisions of these conditions remain in full force and effect."),
            ("12. Test Certificates & Warranty Certificate", "We shall submit our standard Test & Warranty certificate. Any other additional certificate shall be on a chargeable basis and upon acceptance from our end for the same."),
            ("13. Validity", "The Validity of this offer is for a period of 30 days from the date of this offer and shall be extended subjected to mutual acceptance.")
        ]
        
        for title, content in gc_sections:
            story.append(Paragraph(f"<b>{title}</b>", small_bold))
            story.append(Spacer(1, 3))
            story.append(Paragraph(content, small_text))
            story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story, canvasmaker=FooteredCanvas)
        
        return {
            'success': True,
            'filename': filename,
            'filepath': str(filepath.absolute())
        }
        
    except Exception as e:
        import traceback
        return {
            'success': False,
            'message': str(e),
            'traceback': traceback.format_exc()
        }