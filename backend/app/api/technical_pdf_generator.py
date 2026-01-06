"""
Part-Type Specific Technical Quotation PDF Generator
Each part type gets its own PDF with specific template
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from pathlib import Path

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(landscape(A4)[0] - 20, 15, f"Page {self.getPageNumber()} of {page_count}")


def get_field_value(data_dict, *possible_keys):
    """Get field value trying multiple key variations, return '-' if not found"""
    if not data_dict:
        return '-'
    
    for key in possible_keys:
        # Try exact match
        if key in data_dict:
            val = data_dict[key]
            return str(val) if val not in [None, '', 'None', 'null'] else '-'
        
        # Try case-insensitive
        lower_keys = {k.lower(): k for k in data_dict.keys()}
        if key.lower() in lower_keys:
            actual_key = lower_keys[key.lower()]
            val = data_dict[actual_key]
            return str(val) if val not in [None, '', 'None', 'null'] else '-'
    
    return '-'


def add_header_and_metadata(story, title_text, metadata):
    """Add common header and metadata sections"""
    logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
    if not logo_path.exists():
        logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
    
    company_style = ParagraphStyle('Company', fontSize=6.5, alignment=TA_RIGHT, leading=8)
    company_text = """RINGSPANN Power Transmission India Pvt. Ltd.<br/>
Gat No: 679/2/1, Village Kuruli, Taluka Khed,<br/>
Chakan-Alandi Road, District Pune-410501.<br/>
Phone: +91 2135 677500, Fax: +91 2135 677505<br/>
www.ringspann-india.com"""
    
    if logo_path.exists():
        logo = Image(str(logo_path), width=50*mm, height=12*mm)
        header_data = [[logo, Paragraph(company_text, company_style)]]
    else:
        header_data = [["RINGSPANN", Paragraph(company_text, company_style)]]
    
    header_table = Table(header_data, colWidths=[60*mm, 217*mm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    header_box = Table([[header_table]], colWidths=[277*mm])
    header_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(header_box)
    
    # Title
    title_table = Table([[Paragraph(f"<b>{title_text}</b>", 
                        ParagraphStyle('Title', fontSize=10, fontName='Helvetica-Bold', alignment=TA_CENTER))]], 
                        colWidths=[277*mm])
    title_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(title_table)
    
    # Metadata
    meta_style = ParagraphStyle('Meta', fontSize=7.5, leading=10)
    meta_content = f"""<b>Quote number:</b> {metadata.get('quote_number', '')}<br/>
<b>Project name:</b> {metadata.get('project_name', '')}<br/>
<b>End-user name / location:</b> {metadata.get('end_user_name', '')}<br/>
<b>EPC / location:</b> {metadata.get('epc_location', '')}<br/>
<b>OEM name / location:</b> {metadata.get('oem_name', '')}<br/>
<b>Prepared by:</b> {metadata.get('prepared_by', 'Ringspann')}<br/>
<b>Date:</b> {metadata.get('date', datetime.now().strftime('%Y-%m-%d'))}"""
    
    meta_table = Table([[Paragraph(meta_content, meta_style)]], colWidths=[277*mm])
    meta_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(meta_table)


def add_header_and_metadata_wide(story, title_text, metadata, content_width=287):
    """Add header and metadata sections for wider tables (e.g., Locking Element)"""
    logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
    if not logo_path.exists():
        logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
    
    company_style = ParagraphStyle('Company', fontSize=6.5, alignment=TA_RIGHT, leading=8)
    company_text = """RINGSPANN Power Transmission India Pvt. Ltd.<br/>
Gat No: 679/2/1, Village Kuruli, Taluka Khed,<br/>
Chakan-Alandi Road, District Pune-410501.<br/>
Phone: +91 2135 677500, Fax: +91 2135 677505<br/>
www.ringspann-india.com"""
    
    if logo_path.exists():
        logo = Image(str(logo_path), width=50*mm, height=12*mm)
        header_data = [[logo, Paragraph(company_text, company_style)]]
    else:
        header_data = [["RINGSPANN", Paragraph(company_text, company_style)]]
    
    header_table = Table(header_data, colWidths=[60*mm, (content_width-60)*mm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    header_box = Table([[header_table]], colWidths=[content_width*mm])
    header_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(header_box)
    
    # Title
    title_table = Table([[Paragraph(f"<b>{title_text}</b>", 
                        ParagraphStyle('Title', fontSize=10, fontName='Helvetica-Bold', alignment=TA_CENTER))]], 
                        colWidths=[content_width*mm])
    title_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(title_table)
    
    # Metadata
    meta_style = ParagraphStyle('Meta', fontSize=7.5, leading=10)
    meta_content = f"""<b>Quote number:</b> {metadata.get('quote_number', '')}<br/>
<b>Project name:</b> {metadata.get('project_name', '')}<br/>
<b>End-user name / location:</b> {metadata.get('end_user_name', '')}<br/>
<b>EPC / location:</b> {metadata.get('epc_location', '')}<br/>
<b>OEM name / location:</b> {metadata.get('oem_name', '')}<br/>
<b>Prepared by:</b> {metadata.get('prepared_by', 'Ringspann')}<br/>
<b>Date:</b> {metadata.get('date', datetime.now().strftime('%Y-%m-%d'))}"""
    
    meta_table = Table([[Paragraph(meta_content, meta_style)]], colWidths=[content_width*mm])
    meta_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(meta_table)


def add_footer_sections(story, part_type):
    """Add common footer sections"""
    footer_style = ParagraphStyle('Footer', fontSize=6.5, leading=8)
    
    # General points
    general_table = Table([
        [Paragraph('<b>General points</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('1', footer_style), 
         Paragraph('Technical selection are based on information provided in above survey sheet, if any change in value customer to provide same to check selection', footer_style)]
    ], colWidths=[25*mm, 252*mm])
    general_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(general_table)
    
    # Technical points
    tech_points_table = Table([
        [Paragraph('<b>Technical points</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        *[[Paragraph(str(i), footer_style), Paragraph('', footer_style)] for i in range(1, 5)]
    ], colWidths=[25*mm, 252*mm])
    tech_points_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(tech_points_table)
    
    # Revision Status
    revision_table = Table([
        [Paragraph('<b>Revision Status</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('<b>R0</b><br/>Date', footer_style), Paragraph('Initial offer.', footer_style)]
    ], colWidths=[25*mm, 252*mm])
    revision_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(revision_table)
    
    # Issue footer
    issue_text = f'Issue date: {datetime.now().strftime("%d/%b/%y")} Version: 0, Created by: SRK, Checked by: CVS, Doc. No. U 01.458, Description: {part_type} quote template'
    story.append(Paragraph(f'<font size=6>{issue_text}</font>', footer_style))


def add_footer_sections_wide(story, part_type, content_width=287):
    """Add footer sections for wider tables (e.g., Locking Element)"""
    footer_style = ParagraphStyle('Footer', fontSize=6.5, leading=8)
    desc_width = (content_width - 25)  # First column is 25mm
    
    # General points
    general_table = Table([
        [Paragraph('<b>General points</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('1', footer_style), 
         Paragraph('Technical selection are based on information provided in above survey sheet, if any change in value customer to provide same to check selection', footer_style)]
    ], colWidths=[25*mm, desc_width*mm])
    general_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(general_table)
    
    # Technical points
    tech_points_table = Table([
        [Paragraph('<b>Technical points</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        *[[Paragraph(str(i), footer_style), Paragraph('', footer_style)] for i in range(1, 5)]
    ], colWidths=[25*mm, desc_width*mm])
    tech_points_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(tech_points_table)
    
    # Revision Status
    revision_table = Table([
        [Paragraph('<b>Revision Status</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('<b>R0</b><br/>Date', footer_style), Paragraph('Initial offer.', footer_style)]
    ], colWidths=[25*mm, desc_width*mm])
    revision_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(revision_table)
    
    # Issue footer
    issue_text = f'Issue date: {datetime.now().strftime("%d/%b/%y")} Version: 0, Created by: SRK, Checked by: CVS, Doc. No. U 01.458, Description: {part_type} quote template'
    story.append(Paragraph(f'<font size=6>{issue_text}</font>', footer_style))


def generate_brake_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Brake Technical Quotation PDF - BRAKE SPECIFIC TEMPLATE"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING BRAKE TECHNICAL PDF")
    print(f"{'='*60}")
    print(f"Requirements: {len(requirements)}")
    print(f"Technical quotes: {len(technical_quotes)}")
    
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4),
                          rightMargin=10*mm, leftMargin=10*mm,
                          topMargin=10*mm, bottomMargin=15*mm)
    story = []
    
    # Header and metadata
    add_header_and_metadata(story, "BRAKE TECHNICAL QUOTATION", metadata)
    
    # ==================== BRAKE-SPECIFIC TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=5.5, alignment=TA_CENTER, leading=6)
    header_style = ParagraphStyle('HeaderStyle', fontSize=5.5, alignment=TA_CENTER, leading=6, fontName='Helvetica-Bold')
    
    # BRAKE-SPECIFIC COLUMN HEADERS
    header_row = [
        Paragraph('<b>SL<br/>No.</b>', header_style),
        Paragraph('<b>Tag<br/>number</b>', header_style),
        Paragraph('<b>Application</b>', header_style),
        Paragraph('<b>Motor<br/>KW</b>', header_style),
        Paragraph('<b>Number<br/>of<br/>drive</b>', header_style),
        Paragraph('<b>Stopping Torque<br/>(Nm)</b>', header_style),
        '',  # Max
        Paragraph('<b>Speed at brake<br/>(RPM)</b>', header_style),
        '',  # Rated/Max
        '',  # Max
        Paragraph('<b>Stopping<br/>Time</b>', header_style),
        Paragraph('<b>Number of braking<br/>per</b>', header_style),
        '',  # hour
        '',  # day
        Paragraph('<b>Friction<br/>coefficient<br/>between<br/>brake and<br/>brake<br/>disc</b>', header_style),
        Paragraph('<b>Service<br/>factor</b>', header_style),
        Paragraph('<b>Qty</b>', header_style),
        Paragraph('<b>Model</b>', header_style),
        Paragraph('<b>Size</b>', header_style),
        Paragraph('<b>Type</b>', header_style),
        Paragraph('<b>Thruster/<br/>cylinder<br/>size</b>', header_style),
        Paragraph('<b>Material</b>', header_style),
        Paragraph('<b>Accessories</b>', header_style),
        Paragraph('<b>Drum/<br/>Disc<br/>size</b>', header_style),
        Paragraph('<b>Brake<br/>Torque</b>', header_style),
        Paragraph('<b>Theoretical<br/>Stopping<br/>time for<br/>selected<br/>brake</b>', header_style),
        Paragraph('<b>Technical<br/>points</b>', header_style)
    ]
    
    # Sub-headers
    subheader_row = [
        '', '', '', '', '',
        Paragraph('<b>Min</b>', header_style),
        Paragraph('<b>Max</b>', header_style),
        Paragraph('<b>Min</b>', header_style),
        Paragraph('<b>Rated/<br/>Max</b>', header_style),
        Paragraph('<b>Max</b>', header_style),
        Paragraph('<b>sec</b>', header_style),
        Paragraph('<b>sec</b>', header_style),
        Paragraph('<b>hour</b>', header_style),
        Paragraph('<b>day</b>', header_style),
        '', '', '', '', '', '', '', '', '', '', 
        Paragraph('<b>Nm</b>', header_style),
        Paragraph('<b>sec</b>', header_style),
        ''
    ]
    
    table_data = [header_row, subheader_row]
    
    # Add data rows for BRAKE requirements only
    for idx, req in enumerate(requirements):
        req_id = str(req.get('id', ''))
        tech_quote = technical_quotes.get(req_id, {})
        
        cust_reqs = tech_quote.get('customer_requirements', tech_quote.get('customerRequirements', req))
        tech_fields = tech_quote.get('technical_fields', tech_quote.get('technicalFields', tech_quote))
        
        row = [
            Paragraph(str(idx + 1), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tag Number', 'tagNumber', 'tag_number'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Application', 'application'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Motor KW', 'motorKW', 'motor_kw'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Number of Drive', 'numberOfDrive', 'number_of_drive'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Stopping Torque (Mn) Min (Nm)', 'stoppingTorqueMin', 'stopping_torque_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Stopping Torque (Mn) Max (Nm)', 'stoppingTorqueMax', 'stopping_torque_max'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at Brake Min (RPM)', 'speedAtBrakeMin', 'speed_at_brake_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at Brake Rated (RPM)', 'speedAtBrakeRated', 'speed_at_brake_rated'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at Brake Max (RPM)', 'speedAtBrakeMax', 'speed_at_brake_max'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Stopping Time', 'stoppingTime', 'stopping_time'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Number of Braking Per Second', 'brakingPerSecond', 'braking_per_second'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Number of Braking Per Hour', 'brakingPerHour', 'braking_per_hour'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Number of Braking Per Day', 'brakingPerDay', 'braking_per_day'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Friction coefficient between brake and brake disc', 'frictionCoefficient', 'friction_coefficient'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Service Factor', 'serviceFactor', 'service_factor'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Ringspann Product Quantity', 'quantity', 'qty'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Model', 'model'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Size', 'size'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Type', 'type'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Thruster/Cylinder size', 'thrusterSize', 'thruster_size'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Material', 'material'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Accessories', 'accessories'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Drum/Disc size', 'drumDiscSize', 'drum_disc_size'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Brake Torque (Nm)', 'brakeTorque', 'brake_torque'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Theoretical Stopping time for selected brake (sec)', 'theoreticalStoppingTime', 'theoretical_stopping_time'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Technical Points', 'technicalPoints', 'technical_points'), cell_style)
        ]
        table_data.append(row)
    
    # Fill empty rows to 11
    while len(table_data) < 13:
        empty_row = [Paragraph(str(len(table_data) - 1), cell_style)] + [Paragraph('-', cell_style) for _ in range(26)]
        table_data.append(empty_row)
    
    # Total row
    total_row = [''] * 16 + [Paragraph('<b>Total</b>', header_style), Paragraph('<b>0</b>', cell_style)] + [''] * 9
    table_data.append(total_row)
    
    # Column widths for brake template
    col_widths = [
        7*mm, 13*mm, 16*mm, 9*mm, 9*mm, 10*mm, 10*mm, 9*mm, 10*mm, 9*mm,
        9*mm, 8*mm, 8*mm, 8*mm, 12*mm, 9*mm, 8*mm, 11*mm, 9*mm, 9*mm,
        11*mm, 11*mm, 16*mm, 10*mm, 9*mm, 13*mm, 14*mm
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=2)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (0, 0), (0, 1)), ('SPAN', (1, 0), (1, 1)), ('SPAN', (2, 0), (2, 1)),
        ('SPAN', (3, 0), (3, 1)), ('SPAN', (4, 0), (4, 1)), ('SPAN', (5, 0), (6, 0)),
        ('SPAN', (7, 0), (9, 0)), ('SPAN', (10, 0), (10, 1)), ('SPAN', (11, 0), (13, 0)),
        ('SPAN', (14, 0), (14, 1)), ('SPAN', (15, 0), (15, 1)), ('SPAN', (16, 0), (16, 1)),
        ('SPAN', (17, 0), (17, 1)), ('SPAN', (18, 0), (18, 1)), ('SPAN', (19, 0), (19, 1)),
        ('SPAN', (20, 0), (20, 1)), ('SPAN', (21, 0), (21, 1)), ('SPAN', (22, 0), (22, 1)),
        ('SPAN', (23, 0), (23, 1)), ('SPAN', (24, 0), (24, 1)), ('SPAN', (25, 0), (25, 1)),
        ('SPAN', (26, 0), (26, 1)),
        ('FONTSIZE', (0, 0), (-1, -1), 5.5),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    story.append(KeepTogether(main_table))
    add_footer_sections(story, 'Brake')
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Brake PDF generated: {filepath}\n")


def generate_backstop_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Backstop Technical Quotation PDF - EXACT TEMPLATE MATCH"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING BACKSTOP TECHNICAL PDF")
    print(f"{'='*60}")
    print(f"Requirements: {len(requirements)}")
    
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4),
                          rightMargin=10*mm, leftMargin=10*mm,
                          topMargin=10*mm, bottomMargin=15*mm)
    story = []
    
    add_header_and_metadata(story, "BACKSTOP TECHNICAL QUOTATION", metadata)
    
    # ==================== BACKSTOP-SPECIFIC TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=5.5, alignment=TA_CENTER, leading=6)
    header_style = ParagraphStyle('HeaderStyle', fontSize=5.5, alignment=TA_CENTER, leading=6, fontName='Helvetica-Bold')
    
    # BACKSTOP EXACT COLUMNS FROM TEMPLATE
    # Row 1: Main section headers with proper spanning
    
    # First create a spacer row for section headers
    section_row = [
        '',  # SL No (no section header)
        Paragraph('<b>Customer Datasheet</b>', header_style),  # Spans columns 1-10
        '', '', '', '', '', '', '', '', '',
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # Spans columns 11-15
        '', '', '', ''
    ]
    
    # Row 2: Column headers
    header_row = [
        Paragraph('<b>SL No.</b>', header_style),
        Paragraph('<b>Tag<br/>number</b>', header_style),
        Paragraph('<b>Application</b>', header_style),
        Paragraph('<b>Shaft diameter<br/>(d)<br/>mm</b>', header_style),
        Paragraph('<b>Torque<br/>(Mn)</b>', header_style),
        '',  # Max
        Paragraph('<b>Speed</b>', header_style),
        '',  # Rated
        '',  # Max
        Paragraph('<b>Operating<br/>hours<br/>daily</b>', header_style),
        Paragraph('<b>Service<br/>factor</b>', header_style),
        Paragraph('<b>Qty</b>', header_style),
        Paragraph('<b>Product<br/>code</b>', header_style),
        Paragraph('<b>Size</b>', header_style),
        Paragraph('<b>Type</b>', header_style),
        Paragraph('<b>Technical<br/>points</b>', header_style),
    ]
    
    # Sub-headers row
    subheader_row = [
        '',  # SL No
        '',  # Tag number
        '',  # Application
        '',  # Shaft diameter
        Paragraph('<b>Min<br/>Nm</b>', header_style),
        Paragraph('<b>Max<br/>Nm</b>', header_style),
        Paragraph('<b>Min<br/>RPM</b>', header_style),
        Paragraph('<b>Rated</b>', header_style),
        Paragraph('<b>Max</b>', header_style),
        '',  # Operating hours
        '',  # Service factor
        '',  # Qty
        '',  # Product code
        '',  # Size
        '',  # Type
        '',  # Technical points
    ]
    
    table_data = [section_row, header_row, subheader_row]
    
    # Add data rows for BACKSTOP requirements
    for idx, req in enumerate(requirements):
        req_id = str(req.get('id', ''))
        tech_quote = technical_quotes.get(req_id, {})
        
        cust_reqs = tech_quote.get('customer_requirements', tech_quote.get('customerRequirements', req))
        tech_fields = tech_quote.get('technical_fields', tech_quote.get('technicalFields', tech_quote))
        
        row = [
            Paragraph(str(idx + 1), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tag Number', 'tagNumber', 'tag_number'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Application', 'application'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Shaft Diameter (mm)', 'Shaft diameter (d)', 'shaftDiameter', 'shaft_diameter'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque (Mn) Min (Nm)', 'Torque (Mn) Min', 'torqueMin', 'torque_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque (Mn) Max (Nm)', 'Torque (Mn) Max', 'torqueMax', 'torque_max'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Min (RPM)', 'speedMin', 'speed_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Rated (RPM)', 'Speed Rated', 'speedRated', 'speed_rated'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Max (RPM)', 'Speed Max', 'speedMax', 'speed_max'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Operating Hours (daily)', 'Operating hours', 'operatingHours', 'operating_hours'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Service Factor', 'Service factor', 'serviceFactor', 'service_factor'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Ringspann Product Quantity', 'Qty', 'quantity', 'qty'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Product code', 'productCode', 'product_code'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Size', 'size'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Type', 'type'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Technical points', 'technicalPoints', 'technical_points'), cell_style),
        ]
        table_data.append(row)
    
    # Fill empty rows to 3 minimum (as shown in template)
    while len(table_data) < 6:  # 3 header rows + 3 data rows
        empty_row = [Paragraph(str(len(table_data) - 2), cell_style)] + [Paragraph('-', cell_style) for _ in range(15)]
        table_data.append(empty_row)
    
    # Total row
    total_row = [''] * 11 + [Paragraph('<b>Total</b>', header_style), Paragraph('<b>0</b>', cell_style)] + [''] * 3
    table_data.append(total_row)
    
    # Column widths for backstop template (16 columns total = 277mm)
    col_widths = [
        10*mm,   # SL No
        18*mm,   # Tag number
        25*mm,   # Application
        18*mm,   # Shaft diameter
        16*mm,   # Torque Min
        16*mm,   # Torque Max
        16*mm,   # Speed Min
        16*mm,   # Speed Rated
        16*mm,   # Speed Max
        18*mm,   # Operating hours
        16*mm,   # Service factor
        12*mm,   # Qty
        22*mm,   # Product code
        18*mm,   # Size
        18*mm,   # Type
        22*mm,   # Technical points
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=3)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # SECTION HEADER SPANS (Row 0)
        ('SPAN', (0, 0), (0, 2)),   # SL No spans all 3 header rows
        ('SPAN', (1, 0), (10, 0)),  # "Customer Datasheet" spans columns 1-10
        ('SPAN', (11, 0), (15, 0)), # "RINGSPANN Product" spans columns 11-15
        
        # COLUMN HEADER SPANS (Rows 1-2)
        ('SPAN', (1, 1), (1, 2)),   # Tag number
        ('SPAN', (2, 1), (2, 2)),   # Application
        ('SPAN', (3, 1), (3, 2)),   # Shaft diameter
        ('SPAN', (4, 1), (5, 1)),   # Torque (Min, Max)
        ('SPAN', (6, 1), (8, 1)),   # Speed (Min, Rated, Max)
        ('SPAN', (9, 1), (9, 2)),   # Operating hours
        ('SPAN', (10, 1), (10, 2)), # Service factor
        ('SPAN', (11, 1), (11, 2)), # Qty
        ('SPAN', (12, 1), (12, 2)), # Product code
        ('SPAN', (13, 1), (13, 2)), # Size
        ('SPAN', (14, 1), (14, 2)), # Type
        ('SPAN', (15, 1), (15, 2)), # Technical points
        
        # Font and styling
        ('FONTSIZE', (0, 0), (-1, -1), 5.5),
        ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    story.append(KeepTogether(main_table))
    add_footer_sections(story, 'Backstop')
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Backstop PDF generated: {filepath}\n")


def generate_clutch_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Over Running Clutch Technical Quotation PDF - FIXED HEADERS"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING OVER RUNNING CLUTCH TECHNICAL PDF")
    print(f"{'='*60}")
    print(f"Requirements: {len(requirements)}")
    
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4),
                          rightMargin=10*mm, leftMargin=10*mm,
                          topMargin=10*mm, bottomMargin=15*mm)
    story = []
    
    add_header_and_metadata(story, "OVER RUNNING CLUTCH TECHNICAL QUOTATION", metadata)
    
    # ==================== CLUTCH-SPECIFIC TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=5, alignment=TA_CENTER, leading=5.5)
    header_style = ParagraphStyle('HeaderStyle', fontSize=5, alignment=TA_CENTER, leading=5.5, fontName='Helvetica-Bold')
    
    # CLUTCH - CORRECTED 3-ROW HEADER
    
    # Row 0: Main section headers
    section_row = [
        Paragraph('<b>SL<br/>No.</b>', header_style),       # 0
        Paragraph('<b>Tag<br/>number</b>', header_style),   # 1
        Paragraph('<b>Application</b>', header_style),      # 2
        Paragraph('<b>Customer Datasheet</b>', header_style),  # 3-16 (14 empty strings)
        '', '', '', '', '', '', '', '', '', '', '', '', '',
        Paragraph('<b>Operating<br/>hours<br/>daily</b>', header_style),  # 17
        Paragraph('<b>Direction of rotation<br/>from drive side</b>', header_style),  # 18-19 (1 empty string)
        '',
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # 20-22 (2 empty strings)
        '', ''
    ]
    
    # Row 1: Sub-section headers  
    subsection_row = [
        '',  # 0 - SL No (spanned from row 0)
        '',  # 1 - Tag number (spanned from row 0)
        '',  # 2 - Application (spanned from row 0)
        Paragraph('<b>Shaft diameter</b>', header_style),  # 3-6 (3 empty strings)
        '', '', '',
        Paragraph('<b>Torque (Mn)</b>', header_style),  # 7-10 (3 empty strings)
        '', '', '',
        Paragraph('<b>Speed</b>', header_style),  # 11-16 (5 empty strings)
        '', '', '', '', '',
        '',  # 17 - Operating hours (spanned from row 0)
        Paragraph('<b>Main<br/>drive</b>', header_style),      # 18
        Paragraph('<b>Auxiliary<br/>drive</b>', header_style), # 19
        Paragraph('<b>Product<br/>code</b>', header_style),
        Paragraph('<b>Size</b>', header_style),
        Paragraph('<b>Technical<br/>points</b>', header_style),
    ]
    
    # Row 2: Detailed column headers
    detail_row = [
        '',  # 0 - SL No (spanned from row 0)
        '',  # 1 - Tag number (spanned from row 0)
        '',  # 2 - Application (spanned from row 0)
        # Shaft diameter (3-6)
        Paragraph('<b>Main drive<br/>Drive<br/>mm</b>', header_style),
        Paragraph('<b>Main drive<br/>Driven<br/>mm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Drive<br/>mm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Driven<br/>mm</b>', header_style),
        # Torque (7-10)
        Paragraph('<b>Main drive<br/>Min<br/>Nm</b>', header_style),
        Paragraph('<b>Main drive<br/>Max<br/>Nm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Min<br/>Nm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Max<br/>Nm</b>', header_style),
        # Speed (11-16)
        Paragraph('<b>Main drive<br/>Min<br/>RPM</b>', header_style),
        Paragraph('<b>Main drive<br/>Rated</b>', header_style),
        Paragraph('<b>Main drive<br/>Max</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Min<br/>RPM</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Rated</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Max</b>', header_style),
        '',  # 17 - Operating hours (spanned from row 0)
        '',  # 18 - Main drive (spanned from row 1)
        '',  # 19 - Auxiliary drive (spanned from row 1)
        '',  # 20 - Product code (spanned from row 0)
        '',  # 21 - Size (spanned from row 0)
        '',  # 22 - Technical points (spanned from row 0)
    ]
    
    table_data = [section_row, subsection_row, detail_row]
    
    # Add data rows for CLUTCH requirements
    for idx, req in enumerate(requirements):
        req_id = str(req.get('id', ''))
        tech_quote = technical_quotes.get(req_id, {})
        
        cust_reqs = tech_quote.get('customer_requirements', tech_quote.get('customerRequirements', req))
        tech_fields = tech_quote.get('technical_fields', tech_quote.get('technicalFields', tech_quote))
        
        row = [
            Paragraph(str(idx + 1), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tag number', 'tagNumber', 'tag_number'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Application', 'application'), cell_style),
            # Shaft diameter
            Paragraph(get_field_value(cust_reqs, 'Shaft diameter Main drive - Drive (mm)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Shaft diameter Main drive - Driven (mm)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Shaft diameter Auxiliary drive - Drive (mm)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Shaft diameter Auxiliary drive - Driven (mm)'), cell_style),
            # Torque
            Paragraph(get_field_value(cust_reqs, 'Torque Main drive - Min (Nm)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque Main drive - Max (Nm)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque Auxiliary drive - Min (Nm)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque Auxiliary drive - Max (Nm)'), cell_style),
            # Speed
            Paragraph(get_field_value(cust_reqs, 'Speed Main drive - Min (RPM)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Main drive - Rated (RPM)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Main drive - Max (RPM)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Auxiliary drive - Min (RPM)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Auxiliary drive - Rated (RPM)'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed Auxiliary drive - Max (RPM)'), cell_style),
            # Operating & Direction
            Paragraph(get_field_value(cust_reqs, 'Operating hours - daily'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Direction of rotation from drive side - Main drive'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Direction of rotation from drive side - Auxiliary drive'), cell_style),
            # RINGSPANN Product
            Paragraph(get_field_value(tech_fields, 'Product code', 'productCode', 'product_code'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Size', 'size'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Technical points', 'technicalPoints', 'technical_points'), cell_style),
        ]          
        table_data.append(row)
    
    # Fill empty rows to minimum
    while len(table_data) < 7:  # 3 header rows + 4 data rows
        empty_row = [Paragraph(str(len(table_data) - 2), cell_style)] + [Paragraph('-', cell_style) for _ in range(22)]
        table_data.append(empty_row)
    
    # Column widths for clutch template (23 columns total = 277mm)
    col_widths = [
        8*mm,    # SL No
        13*mm,   # Tag number
        17*mm,   # Application
        11*mm,   # Main Drive Drive
        11*mm,   # Main Drive Driven
        11*mm,   # Aux Drive Drive
        11*mm,   # Aux Drive Driven
        11*mm,   # Torque Main Min
        11*mm,   # Torque Main Max
        11*mm,   # Torque Aux Min
        11*mm,   # Torque Aux Max
        11*mm,   # Speed Main Min
        11*mm,   # Speed Main Rated
        11*mm,   # Speed Main Max
        11*mm,   # Speed Aux Min
        11*mm,   # Speed Aux Rated
        11*mm,   # Speed Aux Max
        14*mm,   # Operating hours
        12*mm,   # Direction Main
        12*mm,   # Direction Aux
        17*mm,   # Product code
        12*mm,   # Size
        18*mm,   # Technical points
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=3)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # ROW 0: Main section headers
        ('SPAN', (0, 0), (0, 2)),    # SL No - INDIVIDUAL span
        ('SPAN', (1, 0), (1, 2)),    # Tag number - INDIVIDUAL span
        ('SPAN', (2, 0), (2, 2)),    # Application - INDIVIDUAL span
        ('SPAN', (3, 0), (16, 0)),   # "Customer Datasheet" spans columns 3-16 in row 0
        ('SPAN', (17, 0), (17, 2)),  # Operating hours - INDIVIDUAL span
        ('SPAN', (18, 0), (19, 0)),  # "Direction of rotation" spans columns 18-19 in row 0
        ('SPAN', (20, 0), (22, 0)),  # "RINGSPANN Product" spans columns 20-22 in row 0
        
        # ROW 1: Sub-section headers
        ('SPAN', (3, 1), (6, 1)),    # Shaft diameter spans 4 columns
        ('SPAN', (7, 1), (10, 1)),   # Torque spans 4 columns
        ('SPAN', (11, 1), (16, 1)),  # Speed spans 6 columns
        ('SPAN', (18, 1), (18, 2)),  # Main drive - INDIVIDUAL span to row 2
        ('SPAN', (19, 1), (19, 2)),  # Auxiliary drive - INDIVIDUAL span to row 2
        ('SPAN', (20, 1), (20, 2)),  # Product code - INDIVIDUAL span to row 2
        ('SPAN', (21, 1), (21, 2)),  # Size - INDIVIDUAL span to row 2
        ('SPAN', (22, 1), (22, 2)),  # Technical points - INDIVIDUAL span to row 2
        
        # Font and styling
        ('FONTSIZE', (0, 0), (-1, -1), 5),
        ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 1.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    
    story.append(KeepTogether(main_table))
    add_footer_sections(story, 'Over Running Clutch')
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Over Running Clutch PDF generated: {filepath}\n")



def generate_coupling_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Coupling and Torque Limiter Technical Quotation PDF - EXACT TEMPLATE MATCH"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING COUPLING AND TORQUE LIMITER TECHNICAL PDF")
    print(f"{'='*60}")
    print(f"Requirements: {len(requirements)}")
    
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4),
                          rightMargin=10*mm, leftMargin=10*mm,
                          topMargin=10*mm, bottomMargin=15*mm)
    story = []
    
    add_header_and_metadata(story, "COUPLING AND TORQUE LIMITER TECHNICAL QUOTATION", metadata)
    
    # ==================== COUPLING-SPECIFIC TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=5.5, alignment=TA_CENTER, leading=6)
    header_style = ParagraphStyle('HeaderStyle', fontSize=5.5, alignment=TA_CENTER, leading=6, fontName='Helvetica-Bold')
    
    # COUPLING EXACT COLUMNS FROM TEMPLATE
    # Two-row header structure with section headers
    
    # Row 1: Main section headers
    section_row = [
        Paragraph('<b>SL No.</b>', header_style),  # SL No (spans all 3 rows)
        
        Paragraph('<b>Customer Datasheet</b>', header_style),  # Spans columns 1-9
        '', '', '', '', '', '', '', '',
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # Spans columns 10-13
        '', '', ''
    ]
    
    # Row 2: Column headers
    header_row = [
        '',  # SL No (spanned from row 0)
        Paragraph('<b>Tag<br/>number</b>', header_style),
        Paragraph('<b>Application</b>', header_style),
        Paragraph('<b>Motor<br/>KW</b>', header_style),
        Paragraph('<b>Number of<br/>drive</b>', header_style),
        Paragraph('<b>Torque<br/>(Mn)</b>', header_style),
        '',  # Max
        Paragraph('<b>Speed at coupling</b>', header_style),
        '',  # Rated
        '',  # Max
        Paragraph('<b>Service<br/>factor</b>', header_style),
        Paragraph('<b>Qty</b>', header_style),
        Paragraph('<b>Model</b>', header_style),
        Paragraph('<b>Special<br/>requirement</b>', header_style),
        Paragraph('<b>Technical<br/>points</b>', header_style),
    ]
    
    # Sub-headers row
    subheader_row = [
        '',  # SL No (spanned from row 0)
        '',  # Tag number
        '',  # Application
        '',  # Motor KW
        '',  # Number of drive
        Paragraph('<b>Min<br/>Nm</b>', header_style),
        Paragraph('<b>Max<br/>Nm</b>', header_style),
        Paragraph('<b>Min<br/>RPM</b>', header_style),
        Paragraph('<b>Rated</b>', header_style),
        Paragraph('<b>Max</b>', header_style),
        '',  # Service factor
        '',  # Qty
        '',  # Model
        '',  # Special requirement
        '',  # Technical points
    ]
    
    table_data = [section_row, header_row, subheader_row]
    
    # Add data rows for COUPLING requirements
    for idx, req in enumerate(requirements):
        req_id = str(req.get('id', ''))
        tech_quote = technical_quotes.get(req_id, {})
        
        cust_reqs = tech_quote.get('customer_requirements', tech_quote.get('customerRequirements', req))
        tech_fields = tech_quote.get('technical_fields', tech_quote.get('technicalFields', tech_quote))
        
        row = [
            Paragraph(str(idx + 1), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tag number', 'tagNumber', 'tag_number'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Application', 'application'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Motor KW', 'motorKW', 'motor_kw'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Number of drive', 'numberOfDrive', 'number_of_drive'), cell_style),
            # Torque
            Paragraph(get_field_value(cust_reqs, 'Torque (Mn) Min (Nm)', 'Torque Min', 'torqueMin', 'torque_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque (Mn) Max (Nm)', 'Torque Max', 'torqueMax', 'torque_max'), cell_style),
            # Speed at coupling
            Paragraph(get_field_value(cust_reqs, 'Speed at Coupling Min (RPM)', 'Speed at coupling Min', 'speedMin', 'speed_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at Coupling Rated (RPM)', 'Speed at coupling Rated', 'speedRated', 'speed_rated'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at Coupling Max (RPM)', 'Speed at coupling Max', 'speedMax', 'speed_max'), cell_style),
            # Service factor
            Paragraph(get_field_value(cust_reqs, 'Service factor', 'serviceFactor', 'service_factor'), cell_style),
            # RINGSPANN Product
            Paragraph(get_field_value(tech_fields, 'Ringspann Product Quantity', 'Qty', 'quantity', 'qty'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Model', 'model'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Special Requirements', 'Special requirement', 'specialRequirement', 'special_requirement'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Technical points', 'technicalPoints', 'technical_points'), cell_style),
        ]
        table_data.append(row)
    
    # Fill empty rows to minimum
    while len(table_data) < 6:  # 3 header rows + 3 data rows
        empty_row = [Paragraph(str(len(table_data) - 2), cell_style)] + [Paragraph('-', cell_style) for _ in range(14)]
        table_data.append(empty_row)
    
    # Column widths for coupling template (15 columns total = 277mm)
    col_widths = [
        10*mm,   # SL No
        19*mm,   # Tag number
        26*mm,   # Application
        16*mm,   # Motor KW
        16*mm,   # Number of drive
        18*mm,   # Torque Min
        18*mm,   # Torque Max
        18*mm,   # Speed Min
        18*mm,   # Speed Rated
        18*mm,   # Speed Max
        18*mm,   # Service factor
        12*mm,   # Qty
        22*mm,   # Model
        24*mm,   # Special requirement
        24*mm,   # Technical points
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=3)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # ROW 0: Main section headers
        ('SPAN', (0, 0), (0, 2)),    # SL No spans all 3 header rows
        ('SPAN', (1, 0), (10, 0)),   # "Customer Datasheet" spans columns 1-10
        ('SPAN', (11, 0), (14, 0)),  # "RINGSPANN Product" spans columns 11-14
        
        # ROW 1-2: Column headers
        ('SPAN', (1, 1), (1, 2)),    # Tag number
        ('SPAN', (2, 1), (2, 2)),    # Application
        ('SPAN', (3, 1), (3, 2)),    # Motor KW
        ('SPAN', (4, 1), (4, 2)),    # Number of drive
        ('SPAN', (5, 1), (6, 1)),    # Torque (Min, Max)
        ('SPAN', (7, 1), (9, 1)),    # Speed at coupling (Min, Rated, Max)
        ('SPAN', (10, 1), (10, 2)),  # Service factor
        ('SPAN', (11, 1), (11, 2)),  # Qty
        ('SPAN', (12, 1), (12, 2)),  # Model
        ('SPAN', (13, 1), (13, 2)),  # Special requirement
        ('SPAN', (14, 1), (14, 2)),  # Technical points
        
        # Font and styling
        ('FONTSIZE', (0, 0), (-1, -1), 5.5),
        ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    story.append(KeepTogether(main_table))
    add_footer_sections(story, 'Coupling and Torque Limiter')
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Coupling and Torque Limiter PDF generated: {filepath}\n")

def generate_locking_element_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Locking Element for Conveyor Technical Quotation PDF - CORRECTED STRUCTURE"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING LOCKING ELEMENT FOR CONVEYOR TECHNICAL PDF")
    print(f"{'='*60}")
    print(f"Requirements: {len(requirements)}")
    
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4),
                          rightMargin=5*mm, leftMargin=5*mm,
                          topMargin=10*mm, bottomMargin=15*mm)
    story = []
    
    # Use wide header for locking element (287mm content width)
    add_header_and_metadata_wide(story, "LOCKING ELEMENT FOR CONVEYOR TECHNICAL QUOTATION", metadata, content_width=287)
    
    # ==================== LOCKING ELEMENT-SPECIFIC TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=4, alignment=TA_CENTER, leading=4.5)
    header_style = ParagraphStyle('HeaderStyle', fontSize=4, alignment=TA_CENTER, leading=4.5, fontName='Helvetica-Bold')
    
    # LOCKING ELEMENT - CORRECTED STRUCTURE (31 columns)
    
    # Row 1: Main section headers
    section_row = [
        Paragraph('<b>SL<br/>No.</b>', header_style),
        Paragraph('<b>Pulley<br/>type</b>', header_style),
        Paragraph('<b>Tag<br/>number</b>', header_style),
        Paragraph('<b>Application</b>', header_style),
        Paragraph('<b>Pulley<br/>Qty</b>', header_style),
        Paragraph('<b>Customer Datasheet</b>', header_style),  # 5-19 (15 cols)
        '', '', '', '', '', '', '', '', '', '', '', '', '', '',# 14 empty
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # 20-30 (11 cols)
        '', '', '', '', '', '', '', '', ''
    ]
    
    # Row 2: Sub-section headers
    subsection_row = [
        '',  # 0: SL No (spanned from row 0)
        '',  # 1: Pulley type (spanned from row 0)
        '',  # 2: Tag number (spanned from row 0)
        '',  # 3: Application (spanned from row 0)
        '',  # 4: Pulley Qty (spanned from row 0)
        Paragraph('<b>Hub<br/>material<br/>Yield<br/>strength<br/>(Re)<br/>N/mm2</b>', header_style),
        Paragraph('<b>Shaft<br/>diameter<br/>(d)<br/>mm</b>', header_style),  # 6
        Paragraph('<b>Outer<br/>diameter<br/>pulley<br/>(D2)<br/>mm</b>', header_style),  # 7

        Paragraph('<b>Running condition</b>', header_style),  # 8-9 (2 cols)
        '',
        Paragraph('<b>Starting condition</b>', header_style),  # 10-11 (2 cols)
        '',
        Paragraph('<b>Arm<br/>length<br/>(L)<br/>mm</b>', header_style),
        Paragraph('<b>Wrap<br/>angel<br/>(β)<br/>deg</b>', header_style),  # 13
        Paragraph('<b>start-up<br/>factor<br/>Running<br/>condition</b>', header_style),  # 14
        Paragraph('<b>start-up<br/>factor<br/>starting<br/>condition</b>', header_style),  # 15
        '',  # 15: start-up factor starting
        Paragraph('<b>Running condition</b>', header_style),  # 16-17 (torque, 2 cols)
        '',
        Paragraph('<b>Starting condition</b>', header_style),  # 18-19 (torque, 2 cols)
        '',
        Paragraph('<b>Locking<br/>element<br/>Qty</b>', header_style),  # 20
        Paragraph('<b>Product<br/>code</b>', header_style),  # 21
        Paragraph('<b>Size</b>', header_style),  # 22
        Paragraph('<b>Hub inner<br/>diameter<br/>(Di) mm</b>', header_style),  # 23
        Paragraph('<b>Hub outer<br/>diameter<br/>(Knin) mm</b>', header_style),  # 24
        Paragraph('<b>Hub<br/>length<br/>(Knin) mm</b>', header_style),  # 25
        Paragraph('<b>Torque<br/>(Macl)<br/>Nm</b>', header_style),  # 26
        Paragraph('<b>Bending<br/>moment<br/>(Mb) Nm</b>', header_style),  # 27
        Paragraph('<b>Screw<br/>Tightening<br/>torque<br/>(Ms) Nm</b>', header_style),  # 28
        Paragraph('<b>Shaft<br/>pressure<br/>(Pw)<br/>N/mm2</b>', header_style),  # 29
        Paragraph('<b>Technical<br/>points</b>', header_style),  # 30
    ]
    
    # Row 3: Detailed column headers
    detail_row = [
        '',  # 0: SL No (spanned from row 0)
        '',  # 1: Pulley type (spanned from row 0)
        '',  # 2: Tag number (spanned from row 0)
        '',  # 3: Application (spanned from row 0)
        '',  # 4: Pulley Qty (spanned from row 0)
        Paragraph('<b>Hub<br/>material<br/>Yield<br/>strength<br/>(Re)<br/>N/mm2</b>', header_style),
        Paragraph('<b>Shaft<br/>diameter<br/>(d)<br/>mm</b>', header_style),
        Paragraph('<b>Outer<br/>diameter<br/>pulley<br/>(D2)<br/>mm</b>', header_style),
        # Running condition
        Paragraph('<b>Tension<br/>tight side<br/>(T1)<br/>kN</b>', header_style),
        Paragraph('<b>Tension<br/>slack side<br/>(T2)<br/>kN</b>', header_style),
        # Starting condition
        Paragraph('<b>Tension<br/>tight side<br/>(T1)<br/>kN</b>', header_style),
        Paragraph('<b>Tension<br/>slack side<br/>(T2)<br/>kN</b>', header_style),
        # Additional parameters
        Paragraph('<b>Arm<br/>length<br/>(L)<br/>mm</b>', header_style),
        Paragraph('<b>Wrap<br/>angle<br/>(θ)<br/>deg</b>', header_style),
        Paragraph('<b>start-up<br/>factor<br/>Running<br/>condition</b>', header_style),
        Paragraph('<b>start-up<br/>factor<br/>starting<br/>condition</b>', header_style),
        # Running condition torques
        Paragraph('<b>Torque<br/>(M)<br/>Nm</b>', header_style),
        Paragraph('<b>Bending<br/>moment<br/>(Ms)<br/>Nm</b>', header_style),
        # Starting condition torques
        Paragraph('<b>Torque<br/>(M)<br/>Nm</b>', header_style),
        Paragraph('<b>Bending<br/>moment<br/>(Ms)<br/>Nm</b>', header_style),
        # RINGSPANN Product (spanned from row 1)
        '',  # 20: Locking element Qty
        '',  # 21: Product code
        '',  # 22: Size
        '',  # 23: Hub inner diameter
        '',  # 24: Hub outer diameter
        '',  # 25: Hub length
        '',  # 26: Torque
        '',  # 27: Bending moment
        '',  # 28: Screw Tightening torque
        '',  # 29: Shaft pressure
        '',  # 30: Technical points
    ]
    
    table_data = [section_row, subsection_row, detail_row]
    
    # Add data rows for LOCKING ELEMENT requirements
    for idx, req in enumerate(requirements):
        req_id = str(req.get('id', ''))
        tech_quote = technical_quotes.get(req_id, {})
        
        cust_reqs = tech_quote.get('customer_requirements', tech_quote.get('customerRequirements', req))
        tech_fields = tech_quote.get('technical_fields', tech_quote.get('technicalFields', tech_quote))
        
        row = [
            Paragraph(str(idx + 1), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Pulley type', 'pulleyType', 'pulley_type'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tag number', 'tagNumber', 'tag_number'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Application', 'application'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Pulley Qty', 'pulleyQty', 'pulley_qty'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Hub material Yield strength (Re) N/mm2', 'Hub material Yield strength', 'hubMaterialYieldStrength'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Shaft diameter (d) mm', 'Shaft diameter', 'shaftDiameter'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Outer diameter of pulley (D2) mm', 'Outer diameter pulley', 'outerDiameterPulley'), cell_style),
            # Running condition
            Paragraph(get_field_value(cust_reqs, 'Tension tight side Running condition (T1) KN', 'Running Tension tight side T1'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tension slack side Running condition (T2) KN', 'Running Tension slack side T2'), cell_style),
            # Starting condition
            Paragraph(get_field_value(cust_reqs, 'Tension tight side Starting condition (T1) KN', 'Starting Tension tight side T1'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Tension slack side Starting condition (T2) KN', 'Starting Tension slack side T2'), cell_style),
            # Arm, wrap, factors
            Paragraph(get_field_value(cust_reqs, 'Arm length (L) mm', 'Arm length', 'armLength'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Wrap angel (β) deg', 'Wrap angle', 'wrapAngle'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'start-up factor Running condition', 'Start-up factor Running', 'startUpFactorRunning'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'start-up factor starting condition', 'Start-up factor Starting', 'startUpFactorStarting'), cell_style),
            # Running condition torques
            Paragraph(get_field_value(cust_reqs, 'Torque Running condition (M) Nm', 'Running Torque', 'runningTorque'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Bending moment Running condition (Mb) Nm', 'Running Bending moment', 'runningBendingMoment'), cell_style),
            # Starting condition torques
            Paragraph(get_field_value(cust_reqs, 'Torque Starting condition (M) Nm', 'Starting Torque', 'startingTorque'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Bending moment Starting condition (Mb) Nm', 'Starting Bending moment', 'startingBendingMoment'), cell_style),
            # RINGSPANN Product
            Paragraph(get_field_value(tech_fields, 'Locking element Qty:', 'Locking element Qty', 'lockingElementQty', 'locking_element_qty'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Product code:', 'Product code', 'productCode', 'product_code'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Size:', 'Size', 'size'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Hub inner diameter (Di) mm:', 'Hub inner diameter (Di) mm', 'hubInnerDiameter', 'hub_inner_diameter'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Hub outer diameter (Knin) mm:', 'Hub outer diameter (Knin) mm', 'hubOuterDiameter', 'hub_outer_diameter'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Hub length (Knin) mm:', 'Hub length (Knin) mm', 'hubLength', 'hub_length'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Torque (Macl) Nm:', 'Torque (Macl) Nm', 'torqueMacl', 'torque_macl'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Bending moment (Mb) Nm:', 'Bending moment (Mb) Nm', 'bendingMomentMb', 'bending_moment_mb'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Screw Tightening torque (Ms) Nm:', 'Screw Tightening torque (Ms) Nm', 'screwTighteningTorque', 'screw_tightening_torque'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Shaft pressure (Pw) N/mm2:', 'Shaft pressure (Pw) N/mm2', 'shaftPressure', 'shaft_pressure'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Technical points:', 'Technical points', 'technicalPoints', 'technical_points'), cell_style),
        ]
        table_data.append(row)
    
    # Fill empty rows to minimum
    while len(table_data) < 7:  # 3 header rows + 4 data rows
        empty_row = [Paragraph(str(len(table_data) - 2), cell_style)] + [Paragraph('-', cell_style) for _ in range(30)]
        table_data.append(empty_row)
    
    # Column widths for locking element template (31 columns total = 287mm for 5mm margins)
    col_widths = [
        7*mm,    # SL No
        9*mm,    # Pulley type
        10*mm,   # Tag number
        12*mm,   # Application
        8*mm,    # Pulley Qty
        10*mm,   # Hub material
        9*mm,    # Shaft diameter
        9*mm,    # Outer diameter pulley
        9*mm,    # Running T1
        9*mm,    # Running T2
        9*mm,    # Starting T1
        9*mm,    # Starting T2
        9*mm,    # Arm length
        9*mm,    # Wrap angle
        9*mm,    # Factor running
        9*mm,    # Factor starting
        9*mm,    # Running Torque
        9*mm,    # Running Bending
        9*mm,    # Starting Torque
        9*mm,    # Starting Bending
        9*mm,    # Locking element Qty
        12*mm,   # Product code
        9*mm,    # Size
        9*mm,    # Hub inner
        9*mm,    # Hub outer
        9*mm,    # Hub length
        9*mm,    # Torque Macl
        9*mm,    # Bending Mb
        9*mm,    # Screw torque
        9*mm,    # Shaft pressure
        12*mm,   # Technical points
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=3)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # ROW 0: Main section headers
        ('SPAN', (0, 0), (0, 2)),    # SL No
        ('SPAN', (1, 0), (1, 2)),    # Pulley type
        ('SPAN', (2, 0), (2, 2)),    # Tag number
        ('SPAN', (3, 0), (3, 2)),    # Application
        ('SPAN', (4, 0), (4, 2)),    # Pulley Qty
        ('SPAN', (5, 0), (19, 0)),   # "Customer Datasheet" spans columns 5-19
        ('SPAN', (20, 0), (30, 0)),  # "RINGSPANN Product" spans columns 20-30
        
        # ROW 1: Sub-section headers
        ('SPAN', (5, 1), (5, 2)),    # Hub material
        ('SPAN', (6, 1), (6, 2)),    # Shaft diameter
        ('SPAN', (7, 1), (7, 2)),    # Outer diameter pulley
        ('SPAN', (8, 1), (9, 1)),    # Running condition spans 2
        ('SPAN', (10, 1), (11, 1)),  # Starting condition spans 2
        ('SPAN', (12, 1), (12, 2)),  # Arm length
        ('SPAN', (13, 1), (13, 2)),  # Wrap angle
        ('SPAN', (14, 1), (14, 2)),  # start-up factor Running
        ('SPAN', (15, 1), (15, 2)),  # start-up factor starting
        ('SPAN', (16, 1), (17, 1)),  # Running condition (torque) spans 2
        ('SPAN', (18, 1), (19, 1)),  # Starting condition (torque) spans 2
        ('SPAN', (20, 1), (20, 2)),  # Locking element Qty
        ('SPAN', (21, 1), (21, 2)),  # Product code
        ('SPAN', (22, 1), (22, 2)),  # Size
        ('SPAN', (23, 1), (23, 2)),  # Hub inner diameter
        ('SPAN', (24, 1), (24, 2)),  # Hub outer diameter
        ('SPAN', (25, 1), (25, 2)),  # Hub length
        ('SPAN', (26, 1), (26, 2)),  # Torque
        ('SPAN', (27, 1), (27, 2)),  # Bending moment
        ('SPAN', (28, 1), (28, 2)),  # Screw Tightening torque
        ('SPAN', (29, 1), (29, 2)),  # Shaft pressure
        ('SPAN', (30, 1), (30, 2)),  # Technical points
        
        # Font and styling
        ('FONTSIZE', (0, 0), (-1, -1), 4),
        ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 0.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0.5),
    ]))
    
    story.append(KeepTogether(main_table))
    # Use wide footer for locking element (287mm content width)
    add_footer_sections_wide(story, 'Locking Element for Conveyor', content_width=287)
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Locking Element for Conveyor PDF generated: {filepath}\n")



def generate_technical_pdf_dispatch(quotation_number, metadata, requirements, technical_quotes, output_dir):
    """
    Main dispatcher: Groups requirements by part type and generates separate PDFs
    
    Args:
        quotation_number: Quote number
        metadata: Quote metadata (project, customer, etc)
        requirements: List of ALL requirements
        technical_quotes: Dict of ALL technical quotes
        output_dir: Directory to save PDFs
        
    Returns:
        List of generated PDF file paths
    """
    
    print(f"\n{'='*60}")
    print(f"TECHNICAL PDF GENERATION DISPATCH")
    print(f"{'='*60}")
    print(f"Total requirements: {len(requirements)}")
    print(f"Total technical quotes: {len(technical_quotes)}")
    
    # Group requirements by part type
    grouped_reqs = {}
    for req in requirements:
        part_type = req.get('partType', 'Unknown')
        if part_type not in grouped_reqs:
            grouped_reqs[part_type] = []
        grouped_reqs[part_type].append(req)
    
    print(f"\nGrouped by part type:")
    for part_type, reqs in grouped_reqs.items():
        print(f"  - {part_type}: {len(reqs)} requirements")
    
    generated_files = []
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate separate PDF for each part type
    for part_type, part_reqs in grouped_reqs.items():
        # Filter technical quotes for this part type
        part_tech_quotes = {}
        for req in part_reqs:
            req_id = str(req.get('id', ''))
            if req_id in technical_quotes:
                part_tech_quotes[req_id] = technical_quotes[req_id]
        
        # Generate filename
        part_type_clean = part_type.replace(' ', '_').replace('Quotation', '').strip('_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Technical_Quote_{part_type_clean}_{quotation_number}_{timestamp}.pdf"
        filepath = output_dir / filename
        
        try:
            # Dispatch to appropriate generator
            if 'Brake' in part_type:
                generate_brake_technical_pdf(quotation_number, metadata, part_reqs, part_tech_quotes, filepath)
            elif 'Backstop' in part_type:
                generate_backstop_technical_pdf(quotation_number, metadata, part_reqs, part_tech_quotes, filepath)
            elif 'Clutch' in part_type:
                generate_clutch_technical_pdf(quotation_number, metadata, part_reqs, part_tech_quotes, filepath)
            elif 'Coupling' in part_type or 'Torque Limiter' in part_type:
                generate_coupling_technical_pdf(quotation_number, metadata, part_reqs, part_tech_quotes, filepath)
            elif 'Locking' in part_type or 'Conveyor' in part_type:
                generate_locking_element_technical_pdf(quotation_number, metadata, part_reqs, part_tech_quotes, filepath)
            else:
                print(f"⚠ Unknown part type: {part_type}, using brake template")
                generate_brake_technical_pdf(quotation_number, metadata, part_reqs, part_tech_quotes, filepath)
            
            generated_files.append(str(filepath))
            
        except Exception as e:
            print(f"✗ ERROR generating {part_type} PDF: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Generated {len(generated_files)} PDF(s):")
    for f in generated_files:
        print(f"  ✓ {Path(f).name}")
    print()
    
    return generated_files
