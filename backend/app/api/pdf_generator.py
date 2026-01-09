"""
Commercial Quotation PDF Generator - Exact Format with Logo and Footer
UPDATED: Fixed spacing issues - removed blank pages and excessive whitespace
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether, Frame, PageTemplate
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from pathlib import Path
from app.database.connection import SessionLocal
from sqlalchemy import text

class FooteredCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.logo_path = getattr(FooteredCanvas, '_logo_path', None)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_elements(self, page_count):
        """Draw header and footer on every page"""
        page_width = A4[0]
        page_height = A4[1]
        
        # HEADER (on pages 2+) - FIXED POSITIONING
        if self._pageNumber >= 2:
            if self.logo_path and Path(self.logo_path).exists():
                try:
                    self.drawImage(
                        str(self.logo_path), 
                        page_width - 160,
                        page_height - 55,  # FIXED: Reduced from 60
                        width=130, 
                        height=34,
                        preserveAspectRatio=True
                    )
                except:
                    pass
            
            self.setFont("Helvetica-Bold", 14)
            self.drawString(30, page_height - 45, "RINGSPANN Power Transmission India Pvt. Ltd.")  # FIXED: Reduced from 50
            
            self.setFont("Helvetica-Bold", 16)
            self.drawCentredString(page_width/2, page_height - 70, "Quotation")  # FIXED: Reduced from 80
            
            self.setStrokeColor(colors.black)
            self.setLineWidth(0.5)
            self.line(30, page_height - 75, page_width - 30, page_height - 75)  # FIXED: Reduced from 90
        
        # FOOTER (on all pages)
        self.setFont("Helvetica", 7)
        y_pos = 80
        
        self.drawString(30, y_pos, "RINGSPANN Power Transmission India Pvt. Ltd.")
        self.drawString(30, y_pos-10, "GAT Numbers 679/2/1")
        self.drawString(30, y_pos-20, "Village Kuruli, Taluka Khed, Chakan-Aland Road,")
        self.drawString(30, y_pos-30, "Pune-410501, Maharashtra, INDIA")
        self.drawString(30, y_pos-40, "Phone: +91 2135 677500")
        self.drawString(30, y_pos-50, "Fax: +91 2135 677505")
        self.drawString(30, y_pos-60, "www.ringspann-india.com")
        self.drawString(30, y_pos-70, "info@ringspann-india.com")
        
        self.drawString(220, y_pos, "VAT No.: 27220915992V")
        self.drawString(220, y_pos-10, "CST No.: 27220915992C")
        self.drawString(220, y_pos-20, "ECC Reg. No.: AAFCR486&REM001")
        self.drawString(220, y_pos-30, "Service Tax No.: AAFCR4868R50001")
        self.drawString(220, y_pos-40, "CIN No.: U74900PN2011FTC140818")
        self.drawString(220, y_pos-50, "GSTIN: 27AAFCR4868R1ZD")
        
        self.drawString(410, y_pos, "U.22.715")
        self.drawString(410, y_pos-10, "Axis Bank - Pune 411014")
        self.drawString(410, y_pos-20, "IFSC Code: UTIB0001032")
        self.drawString(410, y_pos-30, "Swift Code: AXISINSB073")
        self.drawString(410, y_pos-40, "Account No. 910020047693645")
        
def flatten_general_conditions(gc_data):
    """Convert hierarchical general conditions to (title, content) tuples for PDF"""
    flattened = []
    
    for section in gc_data:
        number = section["number"]
        title = section["title"]
        content_parts = []
        
        if section.get("content"):
            content_parts.append(section["content"])
        
        if section.get("subsections"):
            for subsection in section["subsections"]:
                letter = subsection.get("letter", "")
                sub_content = subsection.get("content", "")
                content_parts.append(f"<b>{letter}.</b> {sub_content}")
                
                if subsection.get("sub_subsections"):
                    for sub_sub in subsection["sub_subsections"]:
                        roman = sub_sub.get("roman", "")
                        sub_sub_content = sub_sub.get("content", "")
                        content_parts.append(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>({roman})</b> {sub_sub_content}")
        
        full_content = "<br/><br/>".join(content_parts)
        flattened.append((f"{number}. {title}", full_content))
    
    return flattened

def generate_commercial_pdf(quotation_number: str, form_data: dict):
    """Generate PDF matching exact quotation format"""
    try:
        output_dir = Path("data/quotations/commercial")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"Commercial_Quote_{quotation_number.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = output_dir / filename
        
        # FIXED: Reduced topMargin
        doc = BaseDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=95,      # FIXED: Reduced from 110 to 95
            bottomMargin=100
        )
        
        # Frame 1: Single column for first page
        frame_single = Frame(
            doc.leftMargin, 
            doc.bottomMargin, 
            doc.width, 
            doc.height,
            id='single',
            topPadding=0,
            bottomPadding=0,
            leftPadding=0,
            rightPadding=0
        )
        
        # FIXED: Frames for two-column layout - removed unnecessary height adjustment
        frame_width = (doc.width - 10) / 2
        
        frame_left = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            frame_width,
            doc.height,  # FIXED: Removed -110 subtraction
            id='col1',
            topPadding=0,  # FIXED: Changed from 10 to 0
            bottomPadding=0,
            leftPadding=0,
            rightPadding=5
        )
        
        frame_right = Frame(
            doc.leftMargin + frame_width + 10,
            doc.bottomMargin,
            frame_width,
            doc.height,  # FIXED: Removed -110 subtraction
            id='col2',
            topPadding=0,  # FIXED: Changed from 10 to 0
            bottomPadding=0,
            leftPadding=5,
            rightPadding=0
        )
        
        def add_page_elements(canvas, doc):
            pass
        
        template_first = PageTemplate(
            id='FirstPage', 
            frames=[frame_single],
            onPage=add_page_elements,
            pagesize=A4
        )
        
        template_twocol = PageTemplate(
            id='TwoColumn', 
            frames=[frame_left, frame_right],
            onPage=add_page_elements,
            pagesize=A4
        )
        
        doc.addPageTemplates([template_first, template_twocol])
        
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
        
        # Header with logo
        logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
        if not logo_path.exists():
            logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
        
        if logo_path.exists():
            logo = Image(str(logo_path), width=1.8*inch, height=0.47*inch)
            header_table_data = [[
                logo,
                "RINGSPANN Power Transmission India Pvt. Ltd."
            ]]
        else:
            header_table_data = [[
                "RINGSPANN Power Transmission India Pvt. Ltd.",
                ''
            ]]
        
        header_table = Table(header_table_data, colWidths=[1.8*inch, 5.4*inch])
        header_table.setStyle(TableStyle([
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 16),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 5))
        
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
             form_data.get('inquiry_date', datetime.now().strftime('%Y-%m-%d')),
             Paragraph('<b>Date:</b>', small_bold), 
             form_data.get('quotation_date', datetime.now().strftime('%Y-%m-%d'))]
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
        inquiry_date = form_data.get('inquiry_date', datetime.now().strftime('%Y-%m-%d'))
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
        
        # Load custom terms from database
        db = SessionLocal()
        custom_terms_text = None
        try:
            result = db.execute(text("""
                SELECT terms FROM commercial_quotations
                WHERE quotation_number = :quotation_number
            """), {'quotation_number': quotation_number}).fetchone()
            if result and result[0]:
                custom_terms_text = result[0]
                print(f"DEBUG: Loaded custom terms from DB: {custom_terms_text[:100]}...")
            else:
                print(f"DEBUG: No custom terms found for {quotation_number}")
        except Exception as e:
            print(f"Error loading terms: {e}")
        finally:
            db.close()
        
        # Terms
        story.append(Paragraph("<b>Important Commercial Terms</b>", small_bold))
        story.append(Spacer(1, 6))
        
        if custom_terms_text:
            terms = [line for line in custom_terms_text.split('\n') if line.strip()]
            print(f"DEBUG: Using {len(terms)} custom terms")
        else:
            terms = [
                "1) Terms of Payment - 100% against Proforma Invoice.",
                "2) Price basis: Ex-Works Chakan, Pune Basis",
                "3) P&F Charges: 2% Extra on the Basic Price",  # FIXED: Removed semicolon
                "4) Insurance: Shall be borne by you.",
                "5) Taxes:",
                "a) I-GST is applicable for Out of Maharashtra",
                "b) C-GST & S-GST is applicable within the State of Maharashtra.",
                "c) U-GST is applicable for Union Territory.",
                "6) Delivery Period: 8 weeks from date of technically and commercially clear PO.",
                "7) Warranty: 12 months from the date of commissioning or 18 months from the date of Invoice, whichever is earlier."  # FIXED: Changed Warrantee to Warranty
            ]
            print(f"DEBUG: Using default terms")
        
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
        
        # FIXED: Single PageBreak - removed duplicate that caused blank page
        story.append(NextPageTemplate('TwoColumn'))
        story.append(PageBreak())
        
        # PAGE 2+: General Conditions
        # FIXED: Removed Spacer(1, 100) that caused excessive whitespace
        story.append(Paragraph("<b>General Conditions of Delivery and Payment for Customers</b>", small_bold))
        story.append(Spacer(1, 5))
        story.append(Paragraph("The following General Conditions of Delivery and Payment for Customers shall apply to all deliveries of our products, except as modified by express agreement accepted in writing by both parties", small_text))
        story.append(Spacer(1, 10))
        
        # Load custom general conditions
        custom_gc_text = None
        db = SessionLocal()
        try:
            result = db.execute(text("""
                SELECT general_conditions FROM commercial_quotations
                WHERE quotation_number = :quotation_number
            """), {'quotation_number': quotation_number}).fetchone()
            if result and result[0]:
                custom_gc_text = result[0]
                print(f"DEBUG: Loaded custom general conditions from DB")
            else:
                print(f"DEBUG: No custom general conditions found")
        except Exception as e:
            print(f"Error loading general conditions: {e}")
        finally:
            db.close()
        
        # Styles for conditions
        condition_text_style = ParagraphStyle(
            'ConditionText',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            alignment=TA_JUSTIFY,
            spaceBefore=0,
            spaceAfter=0
        )
        
        condition_title_style = ParagraphStyle(
            'ConditionTitle',
            parent=styles['Normal'],
            fontSize=8,
            fontName='Helvetica-Bold',
            leading=10,
            spaceBefore=3,
            spaceAfter=2
        )
        
        # Parse conditions
        if custom_gc_text:
            gc_sections = []
            conditions = custom_gc_text.split('\n\n')
            for condition in conditions:
                if ':' in condition:
                    parts = condition.split(':', 1)
                    gc_sections.append((parts[0].strip(), parts[1].strip()))
        else:
            # Default 12 sections with hierarchical structure
            gc_sections = [
                {
                    "number": "1",
                    "title": "Scope of application",
                    "content": "These Terms apply to the sale and supply of power transmission parts (\"Products\") as per purchase orders issued by the Customer and accepted by the Company. Where applicable, the Company may manufacture or modify Products based on the Customer's specific requirements, subject to a written agreement on design specifications, delivery timelines, and pricing. The following Terms shall apply to all deliveries of our products, except as modified by express agreement accepted in writing by both parties. These Terms do not cover installation, commissioning, or maintenance services, if provided by the Company.",
                    "subsections": []
                },
                {
                    "number": "2",
                    "title": "Definitions",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "Confidential Information shall mean any and all materials and information concerning the Company, including without limitation its directors, officers, employees, subsidiaries and/or group companies, vendors, users and customers or any third party with which the Company associates (collectively, \"Affiliates\"), disclosed by the Company whether or not such information is expressly marked or designated as confidential information, including, without limitation, computer programs, software (including source code, object code and machine code) relating to the foregoing, technical drawings, algorithms, pricing information."
                        },
                        {
                            "letter": "b",
                            "content": "Intellectual Property Rights (IPR) shall mean all drawings, designs, models, specifications, documentation, software, inventions, techniques, processes, business methods, know-how, mask-works, copyrights, copyrightable materials, patents, trademarks, trade secrets, and any other information or materials protected under any intellectual property laws in effect anywhere in the world, and any applications, registrations or filings relating thereto."
                        }
                    ]
                },
                {
                    "number": "3",
                    "title": "Governing Terms",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "The following documents govern the transaction - Any Company-issued quotation, order acknowledgment, invoice, or written agreement."
                        },
                        {
                            "letter": "b",
                            "content": "To the extent possible, the terms contained in these documents shall be read harmoniously. However, in the event of any conflict between these Terms and another document, these Terms shall prevail. These Terms shall prevail over any contrary terms proposed by the Customer. No additional terms shall be deemed part of these Terms unless expressly agreed to in writing and signed by an authorized representative of the Company. For the avoidance of doubt, the following shall not form part of these Terms:",
                            "sub_subsections": [
                                {
                                    "roman": "i",
                                    "content": "Any terms referenced by the Customer in its purchase orders or other documents, except for product description, quantity, and pricing that align with the Company's quotation, acknowledgment, invoice, or a separate signed agreement;"
                                },
                                {
                                    "roman": "ii",
                                    "content": "Customer's standard terms and conditions of purchase, quality policy, supplier guidelines, or similar operational policies;"
                                },
                                {
                                    "roman": "iii",
                                    "content": "Any terms on the Customer's website or electronic procurement portal, even if the Company is required to click \"accept,\" \"agree,\" or similar prompts in order to access or submit order-related information."
                                }
                            ]
                        }
                    ]
                },
                {
                    "number": "4",
                    "title": "Terms of Payment and Pricing",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "Unless otherwise agreed, Customer shall make payment of 100% of the invoiced amount in advance against a Proforma Invoice issued by the Company. In the event of any delay in payment beyond the agreed timeline, the Company reserves the right to charge interest on the overdue amount at a rate of 8% above the prevailing discount rate of the Reserve Bank of India."
                        },
                        {
                            "letter": "b",
                            "content": "The Customer shall not withhold payment or make any deductions from the invoiced amount on account of complaints regarding the Products, unless such liability is acknowledged in writing by the Company. Goods and Services Tax (GST) and any other applicable taxes or duties shall be levied in accordance with the relevant HSN Code and prevailing laws at the time of invoicing."
                        },
                        {
                            "letter": "c",
                            "content": "Unless otherwise agreed in writing, the Company reserves the right to revise prices or apply a surcharge at any time to reflect changes in input costs, including but not limited to raw material prices, labor costs."
                        },
                        {
                            "letter": "d",
                            "content": "In cases where specialized tools, gauges, or clamping devices are required to execute a custom order, such items shall be invoiced separately to the Customer. However, ownership of these tools and devices shall remain exclusively with the Company upon completion of the order. Ownership of the Products shall remain with the Company until full payment of the purchase price has been received."
                        },
                        {
                            "letter": "e",
                            "content": "A Packing and Forwarding (P&F) charge of 2% shall be applicable on the price per Purchase Order. In cases where no P&F charge is applicable, the Company shall utilize its standard packing method for dispatch. Any special packaging requirements requested by the Customer may attract additional charges, which will be communicated separately."
                        }
                    ]
                },
                {
                    "number": "5",
                    "title": "Orders and Acceptance",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "All orders must be submitted in writing and clearly specify the type and quantity of Products, delivery address, required delivery date, and any applicable reference to quotations or prior correspondence."
                        },
                        {
                            "letter": "b",
                            "content": "Orders become binding only upon written acceptance by the Company. All dimensions, weights, illustrations, and technical drawings provided prior to order confirmation are indicative only and not contractually binding, unless confirmed in writing. The scope, specifications, and type of Products to be delivered shall be determined solely by the Company's written order confirmation."
                        },
                        {
                            "letter": "c",
                            "content": "Any modifications requested by the Customer after order confirmation must be approved in writing by the Company and may be subject to revised terms, including pricing and delivery schedule. The Customer may not cancel or amend an order after confirmation without the prior written consent of the Company. Any such change may be subject to charges as reasonably determined by the Company."
                        }
                    ]
                },
                {
                    "number": "6",
                    "title": "Delivery",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "All prices are quoted on an EX Works Chakan basis (Incoterms 2020), unless otherwise agreed."
                        },
                        {
                            "letter": "b",
                            "content": "The delivery period shall commence only after all technical specifications and contractual details have been mutually agreed upon in writing by both Parties"
                        }
                    ]
                },
                {
                    "number": "7",
                    "title": "Force Majeure",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "The Company shall not be liable for any delay in delivery or failure to fulfill an order caused by circumstances beyond its reasonable control, including but not limited to acts of God, natural disasters, pandemics, labor unrest, strikes, lockouts, supply chain disruptions, power or equipment failure, operating difficulties, delays by subcontractors or suppliers, transportation issues, port congestion, embargoes, or any governmental or regulatory actions (\"Force Majeure Event(s)\"). In the event of any such Force Majeure Event(s), the Company shall be entitled to an appropriate extension of the delivery period. The Company will notify the Customer of the occurrence and expected duration of such delay as soon as reasonably practicable. Any claims for penalties, liquidated damages, or other compensation due to delayed delivery shall be excluded unless specifically agreed upon in writing at the time of placing the order. The Customer shall not be entitled to cancel the order, reject, or refuse to accept delivery of the Products due to delays arising from Force Majeure Events or other reasons unless the Products, upon delivery, are found not to conform to the warranty obligations set forth in this Agreement."
                        }
                    ]
                },
                {
                    "number": "8",
                    "title": "Representations and Warranty",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "The Customer shall inspect the Products immediately upon receipt. Any claims for defects or non-conformities must be reported to the Company in writing within seven (7) days of receipt of the shipment. Failure to notify the Company within this period shall constitute acceptance of the Products as delivered and a waiver of any such claims."
                        },
                        {
                            "letter": "b",
                            "content": "Unless otherwise expressly agreed in writing, each Product shall be covered under the limited warranty by the Company that every Product has been been manufactured in accordance with applicable law and that it meets its specifications, it will be free from defects in materials or workmanship, provided it is stored, used and handled under the conditions recommended by Company. The Company warranty is for a period of twelve (12) months from the date of commissioning or eighteen (18) months from the date of dispatch, whichever occurs earlier. In the event of a valid deficiency claim, the Company's sole obligation shall be, at its discretion, to either:",
                            "sub_subsections": [
                                {
                                    "roman": "i",
                                    "content": "Repair the defective component(s), or"
                                },
                                {
                                    "roman": "ii",
                                    "content": "Replace the defective component(s), free of charge, provided that such components are returned to the Company's premises in the original or equivalent protective packaging."
                                }
                            ]
                        },
                        {
                            "letter": "c",
                            "content": "The Company shall be liable only for:",
                            "sub_subsections": [
                                {
                                    "roman": "i",
                                    "content": "Defects arising from its own design or manufacturing faults; and"
                                },
                                {
                                    "roman": "ii",
                                    "content": "Material defects that the Company should have reasonably discovered through due diligence."
                                }
                            ]
                        },
                        {
                            "letter": "d",
                            "content": "The Company shall not be liable for any claims, losses, or damages arising out of or relating to the following circumstances, whether direct or indirect:",
                            "sub_subsections": [
                                {
                                    "roman": "i",
                                    "content": "Normal wear and tear of the Products under regular operating conditions, including deterioration due to environmental exposure, usage, or time;"
                                },
                                {
                                    "roman": "ii",
                                    "content": "Improper handling, incorrect storage, misuse, negligence, or operation of the Products in a manner inconsistent with the Product specifications, manuals, or any written instructions provided by the Company;"
                                },
                                {
                                    "roman": "iii",
                                    "content": "Any modification of the Products undertaken by the Customer or any third party;"
                                },
                                {
                                    "roman": "iv",
                                    "content": "Use of non-original replacement parts, components, or consumables with the Products;"
                                },
                                {
                                    "roman": "v",
                                    "content": "Any force majeure events including but not limited to fire, flood, act of God, civil unrest, strikes, war, pandemic, or government-imposed restrictions;"
                                },
                                {
                                    "roman": "vi",
                                    "content": "Consequential or indirect damages including, but not limited to, loss of production, business interruption, penalties for delay, freight costs, costs of disassembly/reassembly, or damage to other machinery or equipment."
                                },
                                {
                                    "roman": "vii",
                                    "content": "Any claims arising after the expiration of the applicable warranty period."
                                }
                            ]
                        },
                        {
                            "letter": "e",
                            "content": "All other terms and conditions shall be as specified in the Installation and Operating Manual issued by the Company."
                        },
                        {
                            "letter": "f",
                            "content": "The Customer represents that it has all the requisite power to execute these Terms and to perform its obligations hereunder, and the person(s) implementing these Terms on its behalf are duly authorised. These Terms are legally binding upon it and it does not conflict with any agreement, instrument or understanding, oral or written, to which it is a party or by which it may be bound."
                        }
                    ]
                },
                {
                    "number": "9",
                    "title": "Indemnity and Limitation of Liability",
                    "content": "",
                    "subsections": [
                        {
                            "letter": "a",
                            "content": "The Customer shall indemnify and hold harmless the Company and its affiliates (\"Indemnified Parties\") from any claims, losses, liabilities, damages, or expenses (including legal fees) arising from:",
                            "sub_subsections": [
                                {
                                    "roman": "i",
                                    "content": "any breach of these Terms;"
                                },
                                {
                                    "roman": "ii",
                                    "content": "any negligence, willful misconduct, or legal violation by the Customer or its representatives;"
                                },
                                {
                                    "roman": "iii",
                                    "content": "any misuse, unauthorized modification, or improper handling of the Products by the Customer or parties under its control;"
                                },
                                {
                                    "roman": "iv",
                                    "content": "any claim that Customer-provided specifications, drawings, or instructions infringe third-party intellectual property rights."
                                }
                            ]
                        },
                        {
                            "letter": "b",
                            "content": "The Company shall not be liable for any indirect, incidental, consequential, punitive, or special damages, including loss of profits, data, or business, even if advised of such possibility. These limitations and exclusions apply regardless of the form or basis of the claim."
                        }
                    ]
                },
                {
                    "number": "10",
                    "title": "Term and Termination",
                    "content": "These Terms shall remain in effect until completion of the obligations by both Parties and may be terminated earlier by mutual written consent or for material breach not remedied within a reasonable period as discussed in writing by the Customer and the Company.",
                    "subsections": []
                },
                {
                    "number": "11",
                    "title": "Confidentiality Obligations",
                    "content": "The Customer agrees to keep confidential all technical, commercial, and business information received from the Company. The Customer must protect the confidentiality of any information shared by the Company for a period of two (2) years after termination. Breach may result in a fixed penalty (amount to be agreed) per violation, in addition to potential damage claims. The Company also retains the right to claim indemnification of damage caused to it by the disclosure of the information.",
                    "subsections": []
                },
                {
                    "number": "12",
                    "title": "Governing Law and Jurisdiction",
                    "content": "These Terms are governed by the laws of India. Disputes shall be subject to the exclusive jurisdiction of courts in Pune, Maharashtra, India.",
                    "subsections": []
                }
            ]

        # Flatten hierarchical structure
        gc_sections = flatten_general_conditions(gc_sections)
        
        # Add conditions - flows automatically across columns and pages
        for title, content in gc_sections:
            story.append(Paragraph(f"<b>{title}</b>", condition_title_style))
            story.append(Spacer(1, 3))
            story.append(Paragraph(content, condition_text_style))
            story.append(Spacer(1, 10))
        
        # Store logo path as class variable
        FooteredCanvas._logo_path = str(logo_path) if logo_path.exists() else None
        
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














































#-------------------------------------------------------------------------------------------------------------








# """
# Commercial Quotation PDF Generator - Exact Format with Logo and Footer
# """
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
# from reportlab.pdfgen import canvas
# from pathlib import Path
# from app.database.connection import SessionLocal
# from sqlalchemy import text

# class FooteredCanvas(canvas.Canvas):
#     def __init__(self, *args, **kwargs):
#         canvas.Canvas.__init__(self, *args, **kwargs)
#         self._saved_page_states = []

#     def showPage(self):
#         self._saved_page_states.append(dict(self.__dict__))
#         self._startPage()

#     def save(self):
#         num_pages = len(self._saved_page_states)
#         for state in self._saved_page_states:
#             self.__dict__.update(state)
#             self.draw_footer(num_pages)
#             canvas.Canvas.showPage(self)
#         canvas.Canvas.save(self)

#     def draw_footer(self, page_count):
#         page_width = A4[0]
        
#         # Company details footer
#         self.setFont("Helvetica", 7)
#         y_pos = 80
        
#         # Left column
#         self.drawString(30, y_pos, "RINGSPANN Power Transmission India Pvt. Ltd.")
#         self.drawString(30, y_pos-10, "GAT Numbers 679/2/1")
#         self.drawString(30, y_pos-20, "Village Kuruli, Taluka Khed, Chakan-Aland Road,")
#         self.drawString(30, y_pos-30, "Pune-410501, Maharashtra, INDIA")
#         self.drawString(30, y_pos-40, "Phone: +91 2135 677500")
#         self.drawString(30, y_pos-50, "Fax: +91 2135 677505")
#         self.drawString(30, y_pos-60, "www.ringspann-india.com")
#         self.drawString(30, y_pos-70, "info@ringspann-india.com")
        
#         # Middle column
#         self.drawString(220, y_pos, "VAT No.: 27220915992V")
#         self.drawString(220, y_pos-10, "CST No.: 27220915992C")
#         self.drawString(220, y_pos-20, "ECC Reg. No.: AAFCR486&REM001")
#         self.drawString(220, y_pos-30, "Service Tax No.: AAFCR4868R50001")
#         self.drawString(220, y_pos-40, "CIN No.: U74900PN2011FTC140818")
#         self.drawString(220, y_pos-50, "GSTIN: 27AAFCR4868R1ZD")
        
#         # Right column
#         self.drawString(410, y_pos, "U.22.715")
#         self.drawString(410, y_pos-10, "Axis Bank - Pune 411014")
#         self.drawString(410, y_pos-20, "IFSC Code: UTIB0001032")
#         self.drawString(410, y_pos-30, "Swift Code: AXISINSB073")
#         self.drawString(410, y_pos-40, "Account No. 910020047693645")

# def generate_commercial_pdf(quotation_number: str, form_data: dict):
#     """Generate PDF matching exact quotation format"""
#     try:
#         output_dir = Path("data/quotations/commercial")
#         output_dir.mkdir(parents=True, exist_ok=True)
        
#         filename = f"Commercial_Quote_{quotation_number.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         filepath = output_dir / filename
        
#         doc = SimpleDocTemplate(
#             str(filepath),
#             pagesize=A4,
#             rightMargin=30,
#             leftMargin=30,
#             topMargin=30,
#             bottomMargin=100
#         )
        
#         story = []
#         styles = getSampleStyleSheet()
        
#         # Styles
#         company_name_style = ParagraphStyle(
#             'CompanyName',
#             parent=styles['Normal'],
#             fontSize=18,
#             fontName='Helvetica-Bold',
#             alignment=TA_LEFT,
#             spaceAfter=0
#         )
        
#         title_style = ParagraphStyle(
#             'Title',
#             parent=styles['Heading1'],
#             fontSize=18,
#             fontName='Helvetica-Bold',
#             alignment=TA_CENTER,
#             spaceAfter=15,
#             spaceBefore=10
#         )
        
#         small_bold = ParagraphStyle(
#             'SmallBold',
#             parent=styles['Normal'],
#             fontName='Helvetica-Bold',
#             fontSize=8
#         )
        
#         small_text = ParagraphStyle(
#             'Small',
#             parent=styles['Normal'],
#             fontSize=8,
#             leading=11
#         )
        
#         # PAGE 1: Quotation
        
#         # Header with logo and company name
#         logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
#         if not logo_path.exists():
#             # Try alternative path
#             logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
        
#         if logo_path.exists():
#             logo = Image(str(logo_path), width=1.8*inch, height=0.47*inch)
#             header_table_data = [[
#                 "RINGSPANN Power Transmission India Pvt. Ltd.",
#                 logo
#             ]]
#         else:
#             header_table_data = [[
#                 "RINGSPANN Power Transmission India Pvt. Ltd.",
#                 ''
#             ]]
        
#         header_table = Table(header_table_data, colWidths=[5.2*inch, 1.8*inch])
#         header_table.setStyle(TableStyle([
#             ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (0, 0), 16),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('ALIGN', (0, 0), (0, 0), 'LEFT'),
#             ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
#         ]))
        
#         story.append(header_table)
#         story.append(Spacer(1, 5))
        
#         # Title
#         story.append(Paragraph("Quotation", title_style))
        
#         # Contact table
#         contact_data = [
#             [Paragraph('<b>To:</b>', small_bold), form_data.get('to', ''), 
#              Paragraph('<b>Page(s):</b>', small_bold), str(form_data.get('pages', 1))],
#             [Paragraph('<b>Attn.:</b>', small_bold), form_data.get('attn', ''),
#              Paragraph('<b>Your Partner:</b>', small_bold), form_data.get('your_partner', '')],
#             [Paragraph('<b>E-mail:</b>', small_bold), form_data.get('email_to', ''),
#              Paragraph('<b>Mobile No.:</b>', small_bold), form_data.get('mobile_no', '')],
#             [Paragraph('<b>Your Inquiry Ref.:</b>', small_bold), form_data.get('your_inquiry_ref', ''),
#              Paragraph('<b>Fax No.:</b>', small_bold), form_data.get('fax_no', '')],
#             [Paragraph('<b>Quotation No.:</b>', small_bold), quotation_number,
#              Paragraph('<b>E-mail:</b>', small_bold), form_data.get('email_partner', '')],
#             [Paragraph('<b>Inquiry Date:</b>', small_bold), 
#              form_data.get('inquiry_date', datetime.now().strftime('%B %d, %Y')),
#              Paragraph('<b>Date:</b>', small_bold), 
#              form_data.get('quotation_date', datetime.now().strftime('%B %d, %Y'))]
#         ]
        
#         contact_table = Table(contact_data, colWidths=[1.2*inch, 2.3*inch, 1.1*inch, 2.4*inch])
#         contact_table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 0), (-1, -1), 8),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('LEFTPADDING', (0, 0), (-1, -1), 5),
#             ('RIGHTPADDING', (0, 0), (-1, -1), 5),
#             ('TOPPADDING', (0, 0), (-1, -1), 4),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
#         ]))
        
#         story.append(contact_table)
#         story.append(Spacer(1, 15))
        
#         # Greeting
#         inquiry_date = form_data.get('inquiry_date', datetime.now().strftime('%B %d, %Y'))
#         greeting = f"Dear Sir,<br/>This is with reference to your mail enquiry dated on {inquiry_date} we are pleased to offer as under: -"
#         story.append(Paragraph(greeting, small_text))
#         story.append(Spacer(1, 10))
        
#         # Items table
#         items = form_data.get('items', [])
        
#         table_data = [[
#             Paragraph('<b>Sr. No</b>', small_bold),
#             Paragraph('<b>Description</b>', small_bold),
#             Paragraph('<b>Unit Price INR</b>', small_bold),
#             Paragraph('<b>Unit</b>', small_bold),
#             Paragraph('<b>Total Price</b>', small_bold)
#         ]]
        
#         for item in items:
#             desc = f"{item.get('part_type', '')}<br/>{item.get('description', '')}"
#             table_data.append([
#                 str(item.get('sr_no', '')),
#                 Paragraph(desc, small_text),
#                 f"{float(item.get('unit_price', 0)):,.2f}",
#                 str(item.get('unit', 0)),
#                 f"{float(item.get('total_price', 0)):,.2f}"
#             ])
        
#         items_table = Table(table_data, colWidths=[0.5*inch, 3.5*inch, 1.2*inch, 0.6*inch, 1.2*inch])
#         items_table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, -1), 8),
#             ('ALIGN', (0, 0), (0, -1), 'CENTER'),
#             ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
#             ('ALIGN', (3, 0), (3, -1), 'CENTER'),
#             ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('LEFTPADDING', (0, 0), (-1, -1), 5),
#             ('RIGHTPADDING', (0, 0), (-1, -1), 5),
#             ('TOPPADDING', (0, 0), (-1, -1), 6),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#         ]))
        
#         story.append(items_table)
#         story.append(Spacer(1, 15))
        
#         # Load custom terms from database or use defaults
#         db = SessionLocal()
#         custom_terms_text = None
#         try:
#             result = db.execute(text("""
#                 SELECT terms FROM commercial_quotations
#                 WHERE quotation_number = :quotation_number
#             """), {'quotation_number': quotation_number}).fetchone()
#             if result and result[0]:
#                 custom_terms_text = result[0]
#                 print(f"DEBUG: Loaded custom terms from DB: {custom_terms_text[:100]}...")  # Debug
#             else:
#                 print(f"DEBUG: No custom terms found for {quotation_number}")  # Debug
#         except Exception as e:
#             print(f"Error loading terms: {e}")
#         finally:
#             db.close()
        
#         # Terms
#         story.append(Paragraph("<b>Important Commercial Terms</b>", small_bold))
#         story.append(Spacer(1, 6))
        
#         if custom_terms_text:
#             terms = [line for line in custom_terms_text.split('\n') if line.strip()]
#             print(f"DEBUG: Using {len(terms)} custom terms")  # Debug
#         else:
#             terms = [
#                 "1) Terms of Payment - 100% against Proforma Invoice.",
#                 "2) Price basis: Ex-Works Chakan, Pune Basis",
#                 "3) P&F; Charges: 2% Extra on the Basic Price",
#                 "4) Insurance: Shall be borne by you.",
#                 "5) Taxes:",
#                 "a) I-GST is applicable for Out of Maharashtra",
#                 "b) C-GST & S-GST is applicable within the State of Maharashtra.",
#                 "c) U-GST is applicable for Union Territory.",
#                 "6) Delivery Period: 8 weeks from date of technically and commercially clear PO.",
#                 "7) Warrantee/ Guarantee: 12 months from the date of commissioning or 18 months from the date of Invoice, whichever is earlier."
#             ]
#             print(f"DEBUG: Using default terms")  # Debug
        
#         for term in terms:
#             story.append(Paragraph(term, small_text))
#             story.append(Spacer(1, 3))
        
#         story.append(Spacer(1, 10))
#         story.append(Paragraph("Our enclosed General Conditions of Delivery and Payment are applicable.", small_text))
#         story.append(Spacer(1, 10))
#         story.append(Paragraph("We are looking forward to your order.", small_text))
#         story.append(Spacer(1, 8))
#         story.append(Paragraph("Yours sincerely,<br/><b>RINGSPANN Power Transmission India Pvt. Ltd.</b>", small_text))
#         story.append(Spacer(1, 15))
#         story.append(Paragraph("NAME: _________________________", small_text))
#         story.append(Paragraph("DESIGNATION: _________________________", small_text))
        
#         # PAGE BREAK
#         story.append(PageBreak())
        
#         # PAGE 2: General Conditions (same header)
#         # Reuse logo path
#         if not logo_path.exists():
#             logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
#             if not logo_path.exists():
#                 logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
#         story.append(header_table)
#         story.append(Spacer(1, 5))
#         story.append(Paragraph("Quotation", title_style))
#         story.append(Paragraph("<b>General Conditions of Delivery and Payment for Customers</b>", small_bold))
#         story.append(Spacer(1, 5))
#         story.append(Paragraph("The following General Conditions of Delivery and Payment for Customers shall apply to all deliveries of our products, except as modified by express agreement accepted in writing by both parties", small_text))
#         story.append(Spacer(1, 10))
        
#         # Load custom general conditions from database
#         custom_gc_text = None
#         try:
#             result = db.execute(text("""
#                 SELECT general_conditions FROM commercial_quotations
#                 WHERE quotation_number = :quotation_number
#             """), {'quotation_number': quotation_number}).fetchone()
#             if result and result[0]:
#                 custom_gc_text = result[0]
#                 print(f"DEBUG: Loaded custom general conditions from DB")  # Debug
#             else:
#                 print(f"DEBUG: No custom general conditions found")  # Debug
#         except Exception as e:
#             print(f"Error loading general conditions: {e}")
        
#         # Conditions in 2 columns
#         if custom_gc_text:
#             # Parse custom conditions
#             gc_sections = []
#             conditions = custom_gc_text.split('\n\n')
#             for condition in conditions:
#                 if ':' in condition:
#                     parts = condition.split(':', 1)
#                     gc_sections.append((parts[0].strip(), parts[1].strip()))
#         else:
#             # Use default conditions
#             gc_sections = [
#                 ("1. Offer and Conclusion of Contract", "Only our offers and written confirmations will be decisive with respect to the scope and type of products delivered. The contract shall be deemed to have been concluded when we have accepted the order in writing; up to that time our quotation is without obligation. Measures, weights, illustrations and drawings are without obligation for the models, unless expressly confirmed by us in writing. Manufacturing and detail drawings will be supplied by us only if agreed upon before conclusion of the contract and confirmed by us in writing. An appropriate extra charge will be levied for the supply of such drawings. Where special tools and gauges or clamping devices are necessary in order to carry out a special order, these will be invoiced additionally, but shall remain our property after completion of the order."),
#                 ("2. Terms of Delivery", "Prices quoted in our offer are EX Works Chakan Basis. All prices are excluding freight and insurance."),
#                 ("3. Terms of Payment", "The Terms of Payment as applicable is mentioned in our offer. If the terms of payment laid down in the contract are not complied with, interest will be charged at a rate of 8% above the discount rate. In case of complaints with respect to products received, the customer is requested not suspend payment or make any deductions from the invoiced amount, unless liability is admitted by us."),
#                 ("4. Retention of Title/Conditional Sale", "The products shall remain our property until payment has been made in full."),
#                 ("5. Delivery", "The Delivery time is mentioned in our offer. The delivery period shall run from the date on which all technical particulars of the models in questions have been clarified and agreement has been reached between the parties with respect to all details of the contract. In case of unforeseeable circumstances which are beyond our control, i.e., force majeure, operating trouble, delayed deliveries by a subcontractor, rejects in our own plant or at a subcontractor's the delivery period shall be reasonably extended. We shall use our best efforts to honour confirmed delivery dates, which are only approximate. However, if in case of confirmed delivery dates there occurs a delay, an appropriate extension of time shall be granted. Claims for damages or penalties are, therefore, excluded unless its discussed in detail during the placement of the order on us."),
#                 ("6. Packing & Forwarding Charges", "Packing & Forwarding charge @2% shall be applicable on the Basic price of the contract. In case of NIL P & F, then we shall adopt our standard packing method for the dispatch."),
#                 ("7. Taxes", "GST shall be applicable as per the slab of HSN Code."),
#                 ("8. Liability for Defects", "Deficiency claims have to be brought forward immediately upon receipt of the shipment. We warrant the quality of our products in such a manner as to replace or repair all components returned to us because they do not meet the specifications or cannot be used because of defects in workmanship. We accept liability only for defects in design or execution which have been caused by us. For defects in material supplied by us we accept liability only insofar as we should have discovered the deficiency in exercising due diligence. If we are responsible for the technical design, we will accept a deficiency claim only in case the customer can prove that our product does not meet the state of art due to our fault. We are not liable for damages due to normal wear and tear or misuse of the products supplied. Any further claims, such as compensation for direct or indirect damages to machinery or cost incurred in dismantling an assembly work, freight charges or penalties for delay etc. are not covered. Where products have been repaired, altered or overhauled without our consent our liability ceases."),
#                 ("9. Warranty", "Unless otherwise agreed, we warrant the quality of design and manufacture utilizing good raw material for a period of 12 months from the date of commissioning or 18 months from the date of shipment, whichever is earlier, in such a way that we replace or repair free of charge defective components which have been returned to us."),
#                 ("10. Cancellation of Contract", "The customer may cancel the contract only if, upon a reasonable extension of time we have failed to remedy a deficiency or if, in such case, we are, for whatever reason, unable to undertake necessary corrections or to supply a replacement part. In the event that the contract should be cancelled by the customer without our fault, the customer shall reimburse to us, without delay, the invoice value of such contract after deduction of the direct costs saved by us as a result of the cancellation."),
#                 ("11. Purchasing Conditions of Customer", "Purchasing conditions of the customer which are not in compliance with these General Conditions of Delivery and Payment, must be accepted by us in writing in order to be binding. The other provisions of these conditions remain in full force and effect."),
#                 ("12. Test Certificates & Warranty Certificate", "We shall submit our standard Test & Warranty certificate. Any other additional certificate shall be on a chargeable basis and upon acceptance from our end for the same."),
#                 ("13. Validity", "The Validity of this offer is for a period of 30 days from the date of this offer and shall be extended subjected to mutual acceptance.")
#             ]
        
#         for title, content in gc_sections:
#             story.append(Paragraph(f"<b>{title}</b>", small_bold))
#             story.append(Spacer(1, 3))
#             story.append(Paragraph(content, small_text))
#             story.append(Spacer(1, 6))
        
#         # Build PDF
#         doc.build(story, canvasmaker=FooteredCanvas)
        
#         return {
#             'success': True,
#             'filename': filename,
#             'filepath': str(filepath.absolute())
#         }
        
#     except Exception as e:
#         import traceback
#         return {
#             'success': False,
#             'message': str(e),
#             'traceback': traceback.format_exc()
#         }