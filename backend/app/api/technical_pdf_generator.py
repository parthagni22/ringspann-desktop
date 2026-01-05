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
            Paragraph(get_field_value(tech_fields, 'Qty', 'quantity', 'qty'), cell_style),
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
    
    # Column widths for backstop template (16 columns total)
    col_widths = [
        8*mm,   # SL No
        15*mm,  # Tag number
        20*mm,  # Application
        15*mm,  # Shaft diameter
        13*mm,  # Torque Min
        13*mm,  # Torque Max
        13*mm,  # Speed Min
        13*mm,  # Speed Rated
        13*mm,  # Speed Max
        15*mm,  # Operating hours
        13*mm,  # Service factor
        10*mm,  # Qty
        18*mm,  # Product code
        15*mm,  # Size
        15*mm,  # Type
        20*mm,  # Technical points
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
    
    # CLUTCH - SIMPLIFIED 3-ROW HEADER (like Brake template)
    
    # Row 1: Main section headers
    section_row = [
        '',  # SL No
        '',  # Tag number  
        '',  # Application
        Paragraph('<b>Customer Datasheet</b>', header_style),  # Spans shaft/torque/speed columns
        '', '', '', '', '', '', '', '', '', '', '', '', '',
        '',  # Operating hours
        '',  # Direction Main
        '',  # Direction Aux
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # Spans product columns
        '', ''
    ]
    
    # Row 2: Sub-section headers  
    subsection_row = [
        '',  # SL No
        '',  # Tag number
        '',  # Application
        Paragraph('<b>Shaft diameter</b>', header_style),  # Spans 4
        '', '', '',
        Paragraph('<b>Torque (Mn)</b>', header_style),  # Spans 4
        '', '', '',
        Paragraph('<b>Speed</b>', header_style),  # Spans 6
        '', '', '', '', '',
        '',  # Operating hours
        Paragraph('<b>Direction of rotation<br/>from drive side</b>', header_style),  # Spans 2
        '',
        '',  # Product code
        '',  # Size
        '',  # Technical points
    ]
    
    # Row 3: Detailed column headers
    detail_row = [
        Paragraph('<b>SL<br/>No.</b>', header_style),
        Paragraph('<b>Tag<br/>number</b>', header_style),
        Paragraph('<b>Application</b>', header_style),
        # Shaft diameter
        Paragraph('<b>Main drive<br/>Drive<br/>mm</b>', header_style),
        Paragraph('<b>Main drive<br/>Driven<br/>mm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Drive<br/>mm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Driven<br/>mm</b>', header_style),
        # Torque
        Paragraph('<b>Main drive<br/>Min<br/>Nm</b>', header_style),
        Paragraph('<b>Main drive<br/>Max<br/>Nm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Min<br/>Nm</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Max<br/>Nm</b>', header_style),
        # Speed
        Paragraph('<b>Main drive<br/>Min<br/>RPM</b>', header_style),
        Paragraph('<b>Main drive<br/>Rated</b>', header_style),
        Paragraph('<b>Main drive<br/>Max</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Min<br/>RPM</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Rated</b>', header_style),
        Paragraph('<b>Auxiliary drive<br/>Max</b>', header_style),
        # Operating & Direction
        Paragraph('<b>Operating<br/>hours<br/>daily</b>', header_style),
        Paragraph('<b>Main<br/>drive</b>', header_style),
        Paragraph('<b>Auxiliary<br/>drive</b>', header_style),
        # RINGSPANN Product
        Paragraph('<b>Product<br/>code</b>', header_style),
        Paragraph('<b>Size</b>', header_style),
        Paragraph('<b>Technical<br/>points</b>', header_style),
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
    
    # Column widths for clutch template (23 columns total)
    col_widths = [
        8*mm,   # SL No
        12*mm,  # Tag number
        15*mm,  # Application
        10*mm,  # Main Drive Drive
        10*mm,  # Main Drive Driven
        10*mm,  # Aux Drive Drive
        10*mm,  # Aux Drive Driven
        10*mm,  # Torque Main Min
        10*mm,  # Torque Main Max
        10*mm,  # Torque Aux Min
        10*mm,  # Torque Aux Max
        10*mm,  # Speed Main Min
        10*mm,  # Speed Main Rated
        10*mm,  # Speed Main Max
        10*mm,  # Speed Aux Min
        10*mm,  # Speed Aux Rated
        10*mm,  # Speed Aux Max
        12*mm,  # Operating hours
        11*mm,  # Direction Main
        11*mm,  # Direction Aux
        15*mm,  # Product code
        10*mm,  # Size
        15*mm,  # Technical points
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=3)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # ROW 0: Main section headers
        ('SPAN', (0, 0), (2, 2)),    # SL No, Tag, App span all 3 header rows
        ('SPAN', (3, 0), (16, 0)),   # "Customer Datasheet" spans shaft/torque/speed columns
        ('SPAN', (17, 0), (19, 2)),  # Operating & Direction span all 3 rows
        ('SPAN', (20, 0), (22, 0)),  # "RINGSPANN Product" spans product columns
        
        # ROW 1: Sub-section headers
        ('SPAN', (3, 1), (6, 1)),    # Shaft diameter spans 4 columns
        ('SPAN', (7, 1), (10, 1)),   # Torque spans 4 columns
        ('SPAN', (11, 1), (16, 1)),  # Speed spans 6 columns
        ('SPAN', (20, 1), (22, 2)),  # Product fields span to row 2
        
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
        '',  # SL No (spans both rows)
        Paragraph('<b>Customer Datasheet</b>', header_style),  # Spans columns 1-9
        '', '', '', '', '', '', '', '',
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # Spans columns 10-13
        '', '', ''
    ]
    
    # Row 2: Column headers
    header_row = [
        Paragraph('<b>SL No.</b>', header_style),
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
        '',  # SL No
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
            Paragraph(get_field_value(cust_reqs, 'Torque Min', 'torqueMin', 'torque_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Torque Max', 'torqueMax', 'torque_max'), cell_style),
            # Speed at coupling
            Paragraph(get_field_value(cust_reqs, 'Speed at coupling Min', 'speedMin', 'speed_min'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at coupling Rated', 'speedRated', 'speed_rated'), cell_style),
            Paragraph(get_field_value(cust_reqs, 'Speed at coupling Max', 'speedMax', 'speed_max'), cell_style),
            # Service factor
            Paragraph(get_field_value(cust_reqs, 'Service factor', 'serviceFactor', 'service_factor'), cell_style),
            # RINGSPANN Product
            Paragraph(get_field_value(tech_fields, 'Qty', 'quantity', 'qty'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Model', 'model'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Special requirement', 'specialRequirement', 'special_requirement'), cell_style),
            Paragraph(get_field_value(tech_fields, 'Technical points', 'technicalPoints', 'technical_points'), cell_style),
        ]
        table_data.append(row)
    
    # Fill empty rows to minimum
    while len(table_data) < 6:  # 3 header rows + 3 data rows
        empty_row = [Paragraph(str(len(table_data) - 2), cell_style)] + [Paragraph('-', cell_style) for _ in range(14)]
        table_data.append(empty_row)
    
    # Column widths for coupling template (15 columns total)
    col_widths = [
        8*mm,   # SL No
        15*mm,  # Tag number
        20*mm,  # Application
        12*mm,  # Motor KW
        12*mm,  # Number of drive
        13*mm,  # Torque Min
        13*mm,  # Torque Max
        13*mm,  # Speed Min
        13*mm,  # Speed Rated
        13*mm,  # Speed Max
        13*mm,  # Service factor
        10*mm,  # Qty
        18*mm,  # Model
        20*mm,  # Special requirement
        20*mm,  # Technical points
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
    """Generate Locking Element for Conveyor Technical Quotation PDF - 3-ROW HEADER LIKE BACKSTOP"""
    
    print(f"\n{'='*60}")
    print(f"GENERATING LOCKING ELEMENT FOR CONVEYOR TECHNICAL PDF")
    print(f"{'='*60}")
    print(f"Requirements: {len(requirements)}")
    
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4),
                          rightMargin=5*mm, leftMargin=5*mm,
                          topMargin=10*mm, bottomMargin=15*mm)
    story = []
    
    add_header_and_metadata(story, "LOCKING ELEMENT FOR CONVEYOR TECHNICAL QUOTATION", metadata)
    
    # ==================== LOCKING ELEMENT-SPECIFIC TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=4, alignment=TA_CENTER, leading=4.5)
    header_style = ParagraphStyle('HeaderStyle', fontSize=4, alignment=TA_CENTER, leading=4.5, fontName='Helvetica-Bold')
    
    # LOCKING ELEMENT - 3-ROW HEADER (like Backstop) - 31 COLUMNS TOTAL
    
    # Row 1: Main section headers
    section_row = [
        '',  # 0: SL No
        Paragraph('<b>Customer Datasheet</b>', header_style),  # 1-19: spans 19 columns
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        Paragraph('<b>RINGSPANN Product</b>', header_style),  # 20-30: spans 11 columns
        '', '', '', '', '', '', '', '', '', ''
    ]
    
    # Row 2: Column headers with sub-sections
    header_row = [
        Paragraph('<b>SL No.</b>', header_style),  # 0
        Paragraph('<b>Pulley<br/>type</b>', header_style),  # 1
        Paragraph('<b>Tag<br/>number</b>', header_style),  # 2
        Paragraph('<b>Application</b>', header_style),  # 3
        Paragraph('<b>Pulley<br/>Qty</b>', header_style),  # 4
        Paragraph('<b>Hub<br/>material<br/>Yield<br/>strength<br/>(Re)<br/>N/mm2</b>', header_style),  # 5
        Paragraph('<b>Shaft<br/>diameter<br/>(d)<br/>mm</b>', header_style),  # 6
        Paragraph('<b>Outer<br/>diameter<br/>pulley<br/>(D2)<br/>mm</b>', header_style),  # 7
        Paragraph('<b>Running condition</b>', header_style),  # 8-9: spans 2
        '',
        Paragraph('<b>Starting condition</b>', header_style),  # 10-11: spans 2
        '',
        Paragraph('<b>Arm<br/>length<br/>(L)<br/>mm</b>', header_style),  # 12
        Paragraph('<b>Wrap<br/>angle<br/>(θ)<br/>deg</b>', header_style),  # 13
        Paragraph('<b>start-up<br/>factor<br/>Running<br/>condition</b>', header_style),  # 14
        Paragraph('<b>start-up<br/>factor<br/>starting<br/>condition</b>', header_style),  # 15
        Paragraph('<b>Running condition</b>', header_style),  # 16-17: spans 2 (torque)
        '',
        Paragraph('<b>Starting condition</b>', header_style),  # 18-19: spans 2 (torque)
        '',
        Paragraph('<b>Locking<br/>element<br/>Qty</b>', header_style),  # 20
        Paragraph('<b>Product<br/>code</b>', header_style),  # 21
        Paragraph('<b>Size</b>', header_style),  # 22
        Paragraph('<b>Hub<br/>inner<br/>diameter<br/>(D)<br/>mm</b>', header_style),  # 23
        Paragraph('<b>Hub<br/>outer<br/>diameter<br/>(Knm)<br/>mm</b>', header_style),  # 24
        Paragraph('<b>Hub<br/>length<br/>(Knm)<br/>mm</b>', header_style),  # 25
        Paragraph('<b>Torque<br/>(Mnet)<br/>Nm</b>', header_style),  # 26
        Paragraph('<b>Bending<br/>moment<br/>(Ms)<br/>Nm</b>', header_style),  # 27
        Paragraph('<b>Screw<br/>Tightening<br/>torque<br/>(Ms)<br/>Nm</b>', header_style),  # 28
        Paragraph('<b>Shaft<br/>pressure<br/>(Pw)<br/>N/mm2</b>', header_style),  # 29
        Paragraph('<b>Technical<br/>points</b>', header_style),  # 30
    ]
    
    # Row 3: Sub-headers (units/details)
    subheader_row = [
        '',  # 0: SL No
        '',  # 1: Pulley type
        '',  # 2: Tag number
        '',  # 3: Application
        '',  # 4: Pulley Qty
        '',  # 5: Hub material
        '',  # 6: Shaft diameter
        '',  # 7: Outer diameter pulley
        Paragraph('<b>Tension<br/>tight side<br/>(T1)<br/>kN</b>', header_style),  # 8
        Paragraph('<b>Tension<br/>slack side<br/>(T2)<br/>kN</b>', header_style),  # 9
        Paragraph('<b>Tension<br/>tight side<br/>(T1)<br/>kN</b>', header_style),  # 10
        Paragraph('<b>Tension<br/>slack side<br/>(T2)<br/>kN</b>', header_style),  # 11
        '',  # 12: Arm length
        '',  # 13: Wrap angle
        '',  # 14: start-up factor Running
        '',  # 15: start-up factor starting
        Paragraph('<b>Torque<br/>(M)<br/>Nm</b>', header_style),  # 16
        Paragraph('<b>Bending<br/>moment<br/>(Ms)<br/>Nm</b>', header_style),  # 17
        Paragraph('<b>Torque<br/>(M)<br/>Nm</b>', header_style),  # 18
        Paragraph('<b>Bending<br/>moment<br/>(Ms)<br/>Nm</b>', header_style),  # 19
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
    
    table_data = [section_row, header_row, subheader_row]
    
    # Add data rows for LOCKING ELEMENT requirements
    for idx, req in enumerate(requirements):
        req_id = str(req.get('id', ''))
        tech_quote = technical_quotes.get(req_id, {})
        
        cust_reqs = tech_quote.get('customer_requirements', tech_quote.get('customerRequirements', req))
        tech_fields = tech_quote.get('technical_fields', tech_quote.get('technicalFields', tech_quote))
        
        row = [
            Paragraph(str(idx + 1), cell_style),  # 0
            Paragraph(get_field_value(cust_reqs, 'Pulley type', 'pulleyType', 'pulley_type'), cell_style),  # 1
            Paragraph(get_field_value(cust_reqs, 'Tag number', 'tagNumber', 'tag_number'), cell_style),  # 2
            Paragraph(get_field_value(cust_reqs, 'Application', 'application'), cell_style),  # 3
            Paragraph(get_field_value(cust_reqs, 'Pulley Qty', 'pulleyQty', 'pulley_qty'), cell_style),  # 4
            Paragraph(get_field_value(cust_reqs, 'Hub material Yield strength (Re) N/mm2', 'Hub material Yield strength'), cell_style),  # 5
            Paragraph(get_field_value(cust_reqs, 'Shaft diameter (d) mm', 'Shaft diameter'), cell_style),  # 6
            Paragraph(get_field_value(cust_reqs, 'Outer diameter of pulley (D2) mm', 'Outer diameter pulley'), cell_style),  # 7
            # Running condition (2)
            Paragraph(get_field_value(cust_reqs, 'Tension tight side Running condition (T1) KN'), cell_style),  # 8
            Paragraph(get_field_value(cust_reqs, 'Tension slack side Running condition (T2) KN'), cell_style),  # 9
            # Starting condition (2)
            Paragraph(get_field_value(cust_reqs, 'Tension tight side Starting condition (T1) KN'), cell_style),  # 10
            Paragraph(get_field_value(cust_reqs, 'Tension slack side Starting condition (T2) KN'), cell_style),  # 11
            # Parameters
            Paragraph(get_field_value(cust_reqs, 'Arm length (L) mm', 'Arm length'), cell_style),  # 12
            Paragraph(get_field_value(cust_reqs, 'Wrap angel (β) deg', 'Wrap angle'), cell_style),  # 13
            Paragraph(get_field_value(cust_reqs, 'start-up factor Running condition'), cell_style),  # 14
            Paragraph(get_field_value(cust_reqs, 'start-up factor starting condition'), cell_style),  # 15
            # Running condition torques (2)
            Paragraph(get_field_value(cust_reqs, 'Torque Running condition (M) Nm'), cell_style),  # 16
            Paragraph(get_field_value(cust_reqs, 'Bending moment Running condition (Mb) Nm'), cell_style),  # 17
            # Starting condition torques (2)
            Paragraph(get_field_value(cust_reqs, 'Torque Starting condition (M) Nm'), cell_style),  # 18
            Paragraph(get_field_value(cust_reqs, 'Bending moment Starting condition (Mb) Nm'), cell_style),  # 19
            # RINGSPANN Product (11 columns: 20-30)
            Paragraph(get_field_value(tech_fields, 'Locking element Qty', 'lockingElementQty'), cell_style),  # 20
            Paragraph(get_field_value(tech_fields, 'Product code', 'productCode'), cell_style),  # 21
            Paragraph(get_field_value(tech_fields, 'Size', 'size'), cell_style),  # 22
            Paragraph(get_field_value(tech_fields, 'Hub inner diameter (Di) mm', 'Hub inner diameter', 'hubInnerDiameter'), cell_style),  # 23
            Paragraph(get_field_value(tech_fields, 'Hub outer diameter (Knin) mm', 'Hub outer diameter', 'hubOuterDiameter'), cell_style),  # 24
            Paragraph(get_field_value(tech_fields, 'Hub length (Knin) mm', 'Hub length', 'hubLength'), cell_style),  # 25
            Paragraph(get_field_value(tech_fields, 'Torque (Macl) Nm', 'Torque Mnet', 'torqueMnet'), cell_style),  # 26
            Paragraph(get_field_value(tech_fields, 'Bending moment (Mb) Nm', 'Bending moment Ms', 'bendingMomentMs'), cell_style),  # 27
            Paragraph(get_field_value(tech_fields, 'Screw Tightening torque (Ms) Nm', 'Screw Tightening torque', 'screwTighteningTorque'), cell_style),  # 28
            Paragraph(get_field_value(tech_fields, 'Shaft pressure (Pw) N/mm2', 'Shaft pressure', 'shaftPressure'), cell_style),  # 29
            Paragraph(get_field_value(tech_fields, 'Technical points', 'technicalPoints'), cell_style),  # 30
        ]
        table_data.append(row)
    
    # Fill empty rows to minimum
    while len(table_data) < 7:  # 3 header rows + 4 data rows
        empty_row = [Paragraph(str(len(table_data) - 2), cell_style)] + [Paragraph('-', cell_style) for _ in range(30)]
        table_data.append(empty_row)
    
    # Column widths for locking element template (31 columns total)
    col_widths = [
        6*mm,   # 0: SL No
        7*mm,   # 1: Pulley type
        8*mm,   # 2: Tag number
        9*mm,   # 3: Application
        7*mm,   # 4: Pulley Qty
        9*mm,   # 5: Hub material
        8*mm,   # 6: Shaft diameter
        8*mm,   # 7: Outer diameter pulley
        8*mm,   # 8: Running T1
        8*mm,   # 9: Running T2
        8*mm,   # 10: Starting T1
        8*mm,   # 11: Starting T2
        8*mm,   # 12: Arm length
        8*mm,   # 13: Wrap angle
        8*mm,   # 14: Factor running
        8*mm,   # 15: Factor starting
        8*mm,   # 16: Running Torque
        8*mm,   # 17: Running Bending
        8*mm,   # 18: Starting Torque
        8*mm,   # 19: Starting Bending
        7*mm,   # 20: Locking element Qty
        11*mm,  # 21: Product code
        7*mm,   # 22: Size
        8*mm,   # 23: Hub inner
        8*mm,   # 24: Hub outer
        8*mm,   # 25: Hub length
        8*mm,   # 26: Torque Mnet
        8*mm,   # 27: Bending Ms
        8*mm,   # 28: Screw torque
        8*mm,   # 29: Shaft pressure
        10*mm,  # 30: Technical points
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=3)
    main_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # ROW 0: Main section headers
        ('SPAN', (0, 0), (0, 2)),    # SL No spans all 3 header rows
        ('SPAN', (1, 0), (19, 0)),   # "Customer Datasheet" spans columns 1-19 (19 cols)
        ('SPAN', (20, 0), (30, 0)),  # "RINGSPANN Product" spans columns 20-30 (11 cols)
        
        # ROW 1: Column headers with sub-sections
        ('SPAN', (1, 1), (1, 2)),    # Pulley type
        ('SPAN', (2, 1), (2, 2)),    # Tag number
        ('SPAN', (3, 1), (3, 2)),    # Application
        ('SPAN', (4, 1), (4, 2)),    # Pulley Qty
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
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
    ]))
    
    story.append(KeepTogether(main_table))
    add_footer_sections(story, 'Locking Element for Conveyor')
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