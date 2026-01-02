"""
Technical Quotation PDF Generator - Exact Template Match
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
        self.drawRightString(landscape(A4)[0] - 20, 15, f"Page 1 of {page_count}")

def generate_brake_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Brake Technical Quotation PDF matching exact template"""
    
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=landscape(A4),
        rightMargin=10*mm,
        leftMargin=10*mm,
        topMargin=10*mm,
        bottomMargin=15*mm
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # ==================== HEADER SECTION ====================
    # Logo and Company Info
    logo_path = Path("../frontend/public/assets/ringspann_logo2.png")
    if not logo_path.exists():
        logo_path = Path("D:/Irizpro/ringspann-desktop/frontend/public/assets/ringspann_logo2.png")
    
    company_style = ParagraphStyle(
        'Company',
        fontSize=6.5,
        alignment=TA_RIGHT,
        leading=8
    )
    
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
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    # Put header in a box
    header_box_data = [[header_table]]
    header_box = Table(header_box_data, colWidths=[277*mm])
    header_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(header_box)
    
    # Title
    title_data = [[Paragraph("<b>BRAKE TECHNICAL QUOTATION</b>", 
                             ParagraphStyle('Title', fontSize=10, fontName='Helvetica-Bold', alignment=TA_CENTER))]]
    title_table = Table(title_data, colWidths=[277*mm])
    title_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(title_table)
    
    # ==================== METADATA SECTION ====================
    meta_style = ParagraphStyle('Meta', fontSize=7.5, leading=10)
    
    meta_content = f"""<b>Quote number:</b> {metadata.get('quote_number', '')}<br/>
<b>Project name:</b> {metadata.get('project_name', '')}<br/>
<b>End-user name / location:</b> {metadata.get('end_user_name', '')}<br/>
<b>EPC / location:</b> {metadata.get('epc_location', '')}<br/>
<b>OEM name / location:</b> {metadata.get('oem_name', '')}<br/>
<b>Prepared by:</b> {metadata.get('prepared_by', 'Ringspann')}<br/>
<b>Date:</b> {metadata.get('date', datetime.now().strftime('%d %b %Y'))}"""
    
    meta_data = [[Paragraph(meta_content, meta_style)]]
    meta_table = Table(meta_data, colWidths=[277*mm])
    meta_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    story.append(meta_table)
    
    # ==================== MAIN TABLE ====================
    cell_style = ParagraphStyle('CellStyle', fontSize=5.5, alignment=TA_CENTER, leading=6)
    header_style = ParagraphStyle('HeaderStyle', fontSize=5.5, alignment=TA_CENTER, leading=6, fontName='Helvetica-Bold')
    
    # Detailed column headers with proper labels
    header_row = [
        Paragraph('<b>SL<br/>No.</b>', header_style),
        Paragraph('<b>Tag<br/>number</b>', header_style),
        Paragraph('<b>Application</b>', header_style),
        Paragraph('<b>Motor<br/>KW</b>', header_style),
        Paragraph('<b>Number<br/>of<br/>drive</b>', header_style),
        Paragraph('<b>Stopping Torque<br/>(Nm)</b>', header_style),
        '',  # Max column
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
    
    # Sub-headers for split columns
    subheader_row = [
        '',
        '', '', '', '',
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
    
    # Add data rows
    for idx, req in enumerate(requirements):
        if req.get('partType') != 'Brake Quotation':
            continue
    
        # Get requirement ID
        req_id = str(req.get('id', ''))
    
        # Try multiple ways to get the technical quote data
        tech_quote = {}
        if req_id and req_id in technical_quotes:
            tech_quote = technical_quotes[req_id]
        elif idx < len(list(technical_quotes.values())):
            # If keyed differently, try to get by index
            tech_quote = list(technical_quotes.values())[idx]
    
        # Extract customer requirements - try both nested and flat structure
        cust_reqs = {}
        if 'customer_requirements' in tech_quote:
            cust_reqs = tech_quote.get('customer_requirements', {})
        elif 'customerRequirements' in tech_quote:
            cust_reqs = tech_quote.get('customerRequirements', {})
        else:
            # Data might be flat in the requirement itself
            cust_reqs = req
    
        # Extract technical fields - try both nested and flat structure
        tech_fields = {}
        if 'technical_fields' in tech_quote:
            tech_fields = tech_quote.get('technical_fields', {})
        elif 'technicalFields' in tech_quote:
            tech_fields = tech_quote.get('technicalFields', {})
        else:
            tech_fields = tech_quote
    
        # Helper function to safely get value
        def get_val(dict_obj, *keys):
            for key in keys:
                val = dict_obj.get(key, '')
                if val:
                    return val
            return ''
        row = [
            Paragraph(str(idx + 1), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Tag Number', 'tagNumber', 'tag_number')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Application', 'application')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Motor KW', 'motorKW', 'motor_kw')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Number of Drive', 'numberOfDrive', 'number_of_drive')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Stopping Torque (Mn) Min (Nm)', 'stoppingTorqueMin', 'stopping_torque_min')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Stopping Torque (Mn) Max (Nm)', 'stoppingTorqueMax', 'stopping_torque_max')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Speed at Brake Min (RPM)', 'speedAtBrakeMin', 'speed_at_brake_min')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Speed at Brake Rated (RPM)', 'speedAtBrakeRated', 'speed_at_brake_rated')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Speed at Brake Max (RPM)', 'speedAtBrakeMax', 'speed_at_brake_max')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Stopping Time', 'stoppingTime', 'stopping_time')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Number of Braking Per Second', 'brakingPerSecond', 'braking_per_second')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Number of Braking Per Hour', 'brakingPerHour', 'braking_per_hour')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Number of Braking Per Day', 'brakingPerDay', 'braking_per_day')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Friction coefficient between brake and brake disc', 'frictionCoefficient', 'friction_coefficient')), cell_style),
            Paragraph(str(get_val(cust_reqs, 'Service Factor', 'serviceFactor', 'service_factor')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Ringspann Product Quantity', 'quantity', 'qty')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Model', 'model')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Size', 'size')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Type', 'type')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Thruster/Cylinder size', 'thrusterSize', 'thruster_size')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Material', 'material')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Accessories', 'accessories')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Drum/Disc size', 'drumDiscSize', 'drum_disc_size')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Brake Torque (Nm)', 'brakeTorque', 'brake_torque')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Theoretical Stopping time for selected brake (sec)', 'theoreticalStoppingTime', 'theoretical_stopping_time')), cell_style),
            Paragraph(str(get_val(tech_fields, 'Technical Points', 'technicalPoints', 'technical_points')), cell_style)
        ]
        table_data.append(row)
    
    # Add empty rows to make 11 total
    while len(table_data) < 13:  # 2 header rows + 11 data rows
        empty_row = [Paragraph(str(len(table_data) - 1), cell_style)] + ['' for _ in range(26)]
        table_data.append(empty_row)
    
    # Total row
    total_row = [''] * 16 + [Paragraph('<b>Total</b>', header_style), Paragraph('<b>0</b>', cell_style)] + [''] * 9
    table_data.append(total_row)
    
    # Column widths - FIXED to total 277mm to match other boxes
    # Adjusted to exactly match 277mm total width
    col_widths = [
        7*mm,    # SL No
        13*mm,   # Tag number (+1)
        16*mm,   # Application (+1)
        9*mm,    # Motor KW
        9*mm,    # Number of drive
        10*mm,   # Stopping Torque Min
        10*mm,   # Max
        9*mm,    # Speed Min
        10*mm,   # Rated/Max
        9*mm,    # Max
        9*mm,    # Stopping Time
        8*mm,    # per sec
        8*mm,    # per hour
        8*mm,    # per day
        12*mm,   # Friction coefficient
        9*mm,    # Service factor
        8*mm,    # Qty
        11*mm,   # Model
        9*mm,    # Size
        9*mm,    # Type
        11*mm,   # Thruster
        11*mm,   # Material
        16*mm,   # Accessories (+1)
        10*mm,   # Drum/Disc
        9*mm,    # Brake Torque
        13*mm,   # Theoretical time (+1)
        14*mm    # Technical points (+1)
    ]
    
    main_table = Table(table_data, colWidths=col_widths, repeatRows=2)
    main_table.setStyle(TableStyle([
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        # Merge column headers that span multiple subcolumns
        ('SPAN', (0, 0), (0, 1)),   # SL No
        ('SPAN', (1, 0), (1, 1)),   # Tag number
        ('SPAN', (2, 0), (2, 1)),   # Application
        ('SPAN', (3, 0), (3, 1)),   # Motor KW
        ('SPAN', (4, 0), (4, 1)),   # Number of drive
        ('SPAN', (5, 0), (6, 0)),   # Stopping Torque (Min, Max)
        ('SPAN', (7, 0), (9, 0)),   # Speed at brake (Min, Rated/Max, Max)
        ('SPAN', (10, 0), (10, 1)), # Stopping Time
        ('SPAN', (11, 0), (13, 0)), # Number of braking per (sec, hour, day)
        ('SPAN', (14, 0), (14, 1)), # Friction coefficient
        ('SPAN', (15, 0), (15, 1)), # Service factor
        ('SPAN', (16, 0), (16, 1)), # Qty
        ('SPAN', (17, 0), (17, 1)), # Model
        ('SPAN', (18, 0), (18, 1)), # Size
        ('SPAN', (19, 0), (19, 1)), # Type
        ('SPAN', (20, 0), (20, 1)), # Thruster
        ('SPAN', (21, 0), (21, 1)), # Material
        ('SPAN', (22, 0), (22, 1)), # Accessories
        ('SPAN', (23, 0), (23, 1)), # Drum/Disc
        ('SPAN', (24, 0), (24, 1)), # Brake Torque (includes Nm)
        ('SPAN', (25, 0), (25, 1)), # Theoretical time (includes sec)
        ('SPAN', (26, 0), (26, 1)), # Technical points
        # Font
        ('FONTSIZE', (0, 0), (-1, -1), 5.5),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Padding - INCREASED for better spacing
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    # Wrap entire table in KeepTogether to prevent splitting
    story.append(KeepTogether(main_table))
    
    # ==================== FOOTER SECTIONS ====================
    footer_style = ParagraphStyle('Footer', fontSize=6.5, leading=8)
    
    # General points
    general_data = [
        [Paragraph('<b>General points</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('1', footer_style), 
         Paragraph('Technical selection are based on information provided in above survey sheet, if any change in value customer to provide same to check selection', footer_style)]
    ]
    
    general_table = Table(general_data, colWidths=[25*mm, 252*mm])
    general_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(general_table)
    
    # Technical points
    tech_points_data = [
        [Paragraph('<b>Technical points</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('1', footer_style), Paragraph('', footer_style)],
        [Paragraph('2', footer_style), Paragraph('', footer_style)],
        [Paragraph('3', footer_style), Paragraph('', footer_style)],
        [Paragraph('4', footer_style), Paragraph('', footer_style)]
    ]
    
    tech_points_table = Table(tech_points_data, colWidths=[25*mm, 252*mm])
    tech_points_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(tech_points_table)
    
    # Revision Status
    revision_data = [
        [Paragraph('<b>Revision Status</b>', footer_style), Paragraph('<b>Description</b>', footer_style)],
        [Paragraph('<b>R0</b><br/>Date', footer_style), Paragraph('Initial offer.', footer_style)]
    ]
    
    revision_table = Table(revision_data, colWidths=[25*mm, 252*mm])
    revision_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(revision_table)
    
    # Issue date footer
    issue_text = f'Issue date: {datetime.now().strftime("%d/%b/%y")} Version: 0, Created by: SRK, Checked by: CVS, Doc. No. U 01.458, Description: Brake quote template'
    issue_footer = Paragraph(f'<font size=6>{issue_text}</font>', footer_style)
    story.append(issue_footer)
    
    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)

def generate_backstop_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Generate Backstop Technical Quotation PDF"""
    # Similar implementation for backstop
    generate_brake_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath)

def generate_technical_pdf_dispatch(quotation_number, metadata, requirements, technical_quotes, filepath):
    """Dispatch to appropriate PDF generator"""
    if not requirements:
        return False
        
    part_type = requirements[0].get('partType', '')
    
    if 'Brake' in part_type:
        generate_brake_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath)
    elif 'Backstop' in part_type:
        generate_backstop_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath)
    else:
        generate_brake_technical_pdf(quotation_number, metadata, requirements, technical_quotes, filepath)
    
    return True