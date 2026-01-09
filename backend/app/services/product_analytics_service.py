"""
Product Analytics Service - Clean Implementation
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
import json

# Product mapping
PRODUCTS = {
    '1': 'Brake Quotation',
    '2': 'Backstop Quotation',
    '3': 'Couple and Torque Limiter',
    '4': 'Locking Element for Conveyor',
    '5': 'Over Running Clutch'
}

def get_product_name(code):
    return PRODUCTS.get(str(code), 'Unknown')

def get_date_range(filter_type, start, end):
    today = datetime.now().date()
    if filter_type == 'week':
        return today - timedelta(days=7), today
    elif filter_type == 'month':
        return today - timedelta(days=30), today
    elif filter_type == 'quarter':
        return today - timedelta(days=90), today
    elif filter_type == 'year':
        return today - timedelta(days=365), today
    elif filter_type == 'custom' and start and end:
        return datetime.strptime(start, '%Y-%m-%d').date(), datetime.strptime(end, '%Y-%m-%d').date()
    return None, None

def get_product_analytics_updated(db: Session, filters):
    from app.models.project import Project, QuoteStatus
    from app.models.commercial_quotation import CommercialQuotation
    from app.models.technical_quotation import TechnicalQuotation
    
    # Build filters
    conditions = []
    start_date, end_date = get_date_range(filters.date_filter, filters.start_date, filters.end_date)
    
    if start_date and end_date:
        conditions.append(Project.created_at.between(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.max.time())
        ))
    
    if filters.quote_status and filters.quote_status != 'all':
        conditions.append(Project.quote_status == QuoteStatus[filters.quote_status.lower()])
    
    if filters.customer and filters.customer != 'all':
        conditions.append(Project.customer_name == filters.customer)
    
    # Query data
    query = db.query(
        Project.quotation_number,
        Project.customer_name,
        Project.quote_status,
        Project.created_at,
        CommercialQuotation.total_amount
    ).join(CommercialQuotation, Project.quotation_number == CommercialQuotation.quotation_number)
    
    if conditions:
        query = query.filter(and_(*conditions))
    
    projects = query.all()
    
    # Get product types
    tech_map = {t.quotation_number: get_product_name(t.part_type) 
                for t in db.query(TechnicalQuotation.quotation_number, TechnicalQuotation.part_type).all()}
    
    # Process quotes
    all_quotes = []
    won_quotes = []
    
    for p in projects:
        status = p.quote_status.value if hasattr(p.quote_status, 'value') else str(p.quote_status)
        product = tech_map.get(p.quotation_number, 'Unknown')
        
        if filters.product_type and filters.product_type != 'all' and product != filters.product_type:
            continue
        
        quote = {
            'quotation_number': p.quotation_number,
            'customer_name': p.customer_name,
            'quote_status': status,
            'created_at': p.created_at,
            'product_type': product,
            'total_amount': float(p.total_amount or 0)
        }
        
        all_quotes.append(quote)
        if status.lower() == 'won':
            won_quotes.append(quote)
    
    # KPIs
    total_quotes = len(all_quotes)
    total_revenue = sum(q['total_amount'] for q in won_quotes)
    avg_value = sum(q['total_amount'] for q in all_quotes) / total_quotes if total_quotes else 0
    
    product_counts = defaultdict(int)
    for q in all_quotes:
        product_counts[q['product_type']] += 1
    most_quoted = max(product_counts.items(), key=lambda x: x[1])[0] if product_counts else 'N/A'
    
    # Chart 1: Quote counts
    product_quotes = [{'product_type': k, 'quote_count': v} 
                      for k, v in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)]
    
    # Chart 2: Revenue contribution (Won only)
    product_revenue = defaultdict(float)
    for q in won_quotes:
        product_revenue[q['product_type']] += q['total_amount']
    
    total_won = sum(product_revenue.values())
    revenue_contribution = [
        {
            'product_type': k,
            'revenue': round(v, 2),
            'percentage': round((v / total_won * 100), 2) if total_won else 0
        }
        for k, v in sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Chart 3: Monthly trend
    monthly = defaultdict(lambda: defaultdict(int))
    for q in all_quotes:
        if q['created_at']:
            month = q['created_at'].strftime('%Y-%m')
            monthly[month][q['product_type']] += 1
    
    product_trend = [dict(period=m, **counts) for m, counts in sorted(monthly.items())]
    
    # Chart 4: Status breakdown
    status_breakdown = defaultdict(lambda: {'product_type': '', 'Budgetary': 0, 'Active': 0, 'Won': 0, 'Lost': 0})
    for q in all_quotes:
        prod = q['product_type']
        if not status_breakdown[prod]['product_type']:
            status_breakdown[prod]['product_type'] = prod
        if q['quote_status'] in ['Budgetary', 'Active', 'Won', 'Lost']:
            status_breakdown[prod][q['quote_status']] += 1
    
    # Table: Performance
    global_total = sum(float(r.total_amount or 0) 
                      for r in db.query(CommercialQuotation.total_amount).all())
    
    performance = defaultdict(lambda: {'customers': set(), 'won_revenue': 0, 'total': 0})
    for q in all_quotes:
        prod = q['product_type']
        performance[prod]['customers'].add(q['customer_name'])
        performance[prod]['total'] += q['total_amount']
        if q['quote_status'].lower() == 'won':
            performance[prod]['won_revenue'] += q['total_amount']
    
    detailed = [
        {
            'product_type': prod,
            'customer_count': len(data['customers']),
            'won_revenue': round(data['won_revenue'], 2),
            'percentage_of_total': round((data['total'] / global_total * 100), 2) if global_total else 0
        }
        for prod, data in performance.items()
    ]
    detailed.sort(key=lambda x: x['won_revenue'], reverse=True)
    
    return {
        'kpis': {
            'total_quotes': {'label': 'Total Quotes', 'value': total_quotes, 'format_type': 'number'},
            'total_revenue': {'label': 'Total Revenue (Won)', 'value': round(total_revenue, 2), 'format_type': 'currency'},
            'avg_quote_value': {'label': 'Average Quote Value', 'value': round(avg_value, 2), 'format_type': 'currency'},
            'most_quoted_product': {'label': 'Most Quoted Product', 'value': most_quoted, 'format_type': 'text'},
            'product_count': {'label': 'Active Products', 'value': len(product_counts), 'format_type': 'number'}
        },
        'product_quotes': product_quotes,
        'revenue_contribution': revenue_contribution,
        'product_trend': product_trend,
        'status_breakdown': list(status_breakdown.values()),
        'detailed_performance': detailed
    }









# """
# Product Analytics Service - FIXED for missing DB fields
# Uses TechnicalQuotation and CommercialQuotation instead of Project fields
# """
# from sqlalchemy.orm import Session
# from sqlalchemy import func, and_
# from datetime import datetime, timedelta
# from typing import Optional
# from collections import defaultdict
# import json
# # Add product type mapping
# PRODUCT_TYPE_MAP = {
#     '1': 'Brake Quotation',
#     '2': 'Backstop Quotation', 
#     '3': 'Couple and Torque Limiter',
#     '4': 'Locking Element for Conveyor',
#     '5': 'Over Running Clutch'
# }

# def get_product_name(part_type):
#     """Convert part_type code to readable name"""
#     if not part_type:
#         return 'Unknown'
#     return PRODUCT_TYPE_MAP.get(str(part_type), f'Product {part_type}')

# def get_date_range(date_filter: str, start_date: Optional[str], end_date: Optional[str]):
#     """Helper to get date range filter"""
#     today = datetime.now().date()
    
#     if date_filter == 'week':
#         return today - timedelta(days=7), today
#     elif date_filter == 'month':
#         return today - timedelta(days=30), today
#     elif date_filter == 'quarter':
#         return today - timedelta(days=90), today
#     elif date_filter == 'year':
#         return today - timedelta(days=365), today
#     elif date_filter == 'custom' and start_date and end_date:
#         return datetime.strptime(start_date, '%Y-%m-%d').date(), datetime.strptime(end_date, '%Y-%m-%d').date()
#     else:
#         return None, None


# def get_product_analytics_updated(db: Session, filters):
#     """
#     FIXED: Get analytics from CommercialQuotation.items + TechnicalQuotation.part_type
#     Since Project doesn't have product_type, quotation_date, total_price
#     """
#     from app.models.project import Project
#     from app.models.commercial_quotation import CommercialQuotation
#     from app.models.technical_quotation import TechnicalQuotation
    
#     # Build base filters
#     query_filters = []
    
#     # Date filter (use Project.created_at instead of quotation_date)
#     start_date, end_date = get_date_range(filters.date_filter, filters.start_date, filters.end_date)
#     if start_date and end_date:
#         query_filters.append(Project.created_at.between(
#             datetime.combine(start_date, datetime.min.time()),
#             datetime.combine(end_date, datetime.max.time())
#         ))
    
#     # Status filter
#     if filters.quote_status and filters.quote_status != 'all':
#         query_filters.append(Project.quote_status == filters.quote_status)
    
#     # Customer filter
#     if filters.customer and filters.customer != 'all':
#         query_filters.append(Project.customer_name == filters.customer)
    
#     # Get all projects with commercial quotes
#     query = db.query(
#         Project.id,
#         Project.quotation_number,
#         Project.customer_name,
#         Project.quote_status,
#         Project.created_at,
#         CommercialQuotation.items,
#         CommercialQuotation.total_amount
#     ).join(
#         CommercialQuotation,
#         Project.quotation_number == CommercialQuotation.quotation_number
#     )
    
#     if query_filters:
#         query = query.filter(and_(*query_filters))
    
#     all_projects = query.all()
    
#     # Get technical quotes for product types
#     tech_quotes = db.query(
#         TechnicalQuotation.quotation_number,
#         TechnicalQuotation.part_type
#     ).all()
    
#     tech_map = {t.quotation_number: t.part_type for t in tech_quotes}
    
#     # Process data
#     all_quotes_data = []
#     won_quotes_data = []
    
#     for proj in all_projects:
#         # Parse items
#         try:
#             items = json.loads(proj.items) if proj.items else []
#         except:
#             items = []
        
#         # Get product type from technical quote
#         product_type = tech_map.get(proj.quotation_number, 'Unknown')
        
#         # Apply product filter
#         if filters.product_type and filters.product_type != 'all':
#             if product_type != filters.product_type:
#                 continue
        
#         quote_data = {
#             'quotation_number': proj.quotation_number,
#             'customer_name': proj.customer_name,
#             'quote_status': proj.quote_status,
#             'created_at': proj.created_at,
#             'product_type': product_type,
#             'total_amount': float(proj.total_amount or 0),
#             'items': items
#         }
        
#         all_quotes_data.append(quote_data)
        
#         if proj.quote_status == 'Won':
#             won_quotes_data.append(quote_data)
    
#     print(f"DEBUG: all_quotes={len(all_quotes_data)}, won_quotes={len(won_quotes_data)}")
    
#     # === KPI CALCULATIONS ===
#     total_quotes = len(all_quotes_data)
#     total_revenue = sum(q['total_amount'] for q in won_quotes_data)
#     avg_quote_value = sum(q['total_amount'] for q in all_quotes_data) / total_quotes if total_quotes > 0 else 0
    
#     # Most quoted product
#     product_counts = defaultdict(int)
#     for q in all_quotes_data:
#         product_counts[q['product_type']] += 1
#     most_quoted = max(product_counts.items(), key=lambda x: x[1])[0] if product_counts else 'N/A'
    
#     # Active products
#     active_products = len(set(q['product_type'] for q in all_quotes_data))
    
#     # === CHART 1: Product Quote Count ===
#     product_quotes = [
#         {'product_type': k, 'quote_count': v}
#         for k, v in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
#     ]
    
#     # === CHART 2: Revenue Contribution (Won) - FROM ITEMS ===
#     product_revenue = defaultdict(float)
    
#     for q in won_quotes_data:
#         # Aggregate by items in quote
#         for item in q['items']:
#             part_type = item.get('part_type', item.get('description', 'Unknown'))
#             total_price = float(item.get('total_price', 0))
#             product_revenue[part_type] += total_price
    
#     total_won_revenue = sum(product_revenue.values())
    
#     revenue_contribution = [
#         {
#             'product_type': k,
#             'revenue': v,
#             'percentage': (v / total_won_revenue * 100) if total_won_revenue > 0 else 0
#         }
#         for k, v in sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
#     ]
    
#     # === CHART 3: Monthly Trend ===
#     monthly_data = defaultdict(lambda: defaultdict(int))
#     for q in all_quotes_data:
#         if q['created_at']:
#             month = q['created_at'].strftime('%Y-%m')
#             product = q['product_type']
#             monthly_data[month][product] += 1
    
#     product_trend = []
#     for month in sorted(monthly_data.keys()):
#         point = {'period': month}
#         for product, count in monthly_data[month].items():
#             point[product] = count
#         product_trend.append(point)
    
#     # === CHART 4: Status Breakdown ===
#     status_data = defaultdict(lambda: {'product_type': '', 'Budgetary': 0, 'Active': 0, 'Won': 0, 'Lost': 0})
#     for q in all_quotes_data:
#         product = q['product_type']
#         status = q['quote_status']
        
#         if product not in status_data:
#             status_data[product]['product_type'] = product
        
#         if status in ['Budgetary', 'Active', 'Won', 'Lost']:
#             status_data[product][status] += 1
    
#     status_breakdown = list(status_data.values())
    
#     # === TABLE: Detailed Performance ===
#     global_query = db.query(CommercialQuotation.total_amount)
#     if start_date and end_date:
#         global_query = global_query.join(Project).filter(
#             Project.created_at.between(
#                 datetime.combine(start_date, datetime.min.time()),
#                 datetime.combine(end_date, datetime.max.time())
#             )
#         )
    
#     global_total = sum(float(row.total_amount or 0) for row in global_query.all())
    
#     product_performance = defaultdict(lambda: {'customers': set(), 'won_revenue': 0, 'total_quoted': 0})
    
#     for q in all_quotes_data:
#         product = q['product_type']
        
#         product_performance[product]['customers'].add(q['customer_name'])
#         product_performance[product]['total_quoted'] += q['total_amount']
        
#         if q['quote_status'] == 'Won':
#             product_performance[product]['won_revenue'] += q['total_amount']
    
#     detailed_performance = [
#         {
#             'product_type': product,
#             'customer_count': len(data['customers']),
#             'won_revenue': data['won_revenue'],
#             'percentage_of_total': (data['total_quoted'] / global_total * 100) if global_total > 0 else 0
#         }
#         for product, data in product_performance.items()
#     ]
#     detailed_performance.sort(key=lambda x: x['won_revenue'], reverse=True)
    
#     return {
#         'kpis': {
#             'total_quotes': {
#                 'label': 'Total Quotes',
#                 'value': total_quotes,
#                 'format_type': 'number',
#                 'change_percent': None,
#                 'change_direction': None
#             },
#             'total_revenue': {
#                 'label': 'Total Revenue (Won)',
#                 'value': round(total_revenue, 2),
#                 'format_type': 'currency',
#                 'change_percent': None,
#                 'change_direction': None
#             },
#             'avg_quote_value': {
#                 'label': 'Average Quote Value',
#                 'value': round(avg_quote_value, 2),
#                 'format_type': 'currency',
#                 'change_percent': None,
#                 'change_direction': None
#             },
#             'most_quoted_product': {
#                 'label': 'Most Quoted Product',
#                 'value': most_quoted,
#                 'format_type': 'text'
#             },
#             'product_count': {
#                 'label': 'Active Products',
#                 'value': active_products,
#                 'format_type': 'number'
#             }
#         },
#         'product_quotes': product_quotes,
#         'revenue_contribution': revenue_contribution,
#         'product_trend': product_trend,
#         'status_breakdown': status_breakdown,
#         'detailed_performance': detailed_performance
#     }













# """
# Product Analytics Service - Updated Requirements
# Separate file to avoid breaking existing analytics_service.py
# """
# from sqlalchemy.orm import Session
# from sqlalchemy import func, and_
# from datetime import datetime, timedelta
# from typing import Optional
# from collections import defaultdict


# def get_date_range(date_filter: str, start_date: Optional[str], end_date: Optional[str]):
#     """Helper to get date range filter"""
#     today = datetime.now().date()
    
#     if date_filter == 'week':
#         return today - timedelta(days=7), today
#     elif date_filter == 'month':
#         return today - timedelta(days=30), today
#     elif date_filter == 'quarter':
#         return today - timedelta(days=90), today
#     elif date_filter == 'year':
#         return today - timedelta(days=365), today
#     elif date_filter == 'custom' and start_date and end_date:
#         return datetime.strptime(start_date, '%Y-%m-%d').date(), datetime.strptime(end_date, '%Y-%m-%d').date()
#     else:
#         return None, None


# def get_product_analytics_updated(db: Session, filters):
#     """
#     Updated product analytics with new requirements:
#     1. Total Revenue = Won quotes only
#     2. Avg Quote Value = all quotes formula
#     3. Product quotes count (all statuses)
#     4. Revenue contribution (Won only)
#     5. Table: Customer count, Won revenue, % of total
#     """
#     from app.models.project import Project
    
#     # Build base query
#     query_filters = []
    
#     # Date filter
#     start_date, end_date = get_date_range(filters.date_filter, filters.start_date, filters.end_date)
#     if start_date and end_date:
#         query_filters.append(Project.quotation_date.between(start_date, end_date))
    
#     # Status filter
#     if filters.quote_status and filters.quote_status != 'all':
#         query_filters.append(Project.quote_status == filters.quote_status)
    
#     # Product Type filter
#     if filters.product_type and filters.product_type != 'all':
#         query_filters.append(Project.product_type == filters.product_type)
    
#     # Customer filter
#     if filters.customer and filters.customer != 'all':
#         query_filters.append(Project.customer_name == filters.customer)
    
#     # Get all quotes matching filters
#     all_quotes = db.query(Project).filter(and_(*query_filters)).all() if query_filters else db.query(Project).all()
    
#     # Get won quotes only
#     won_filters = query_filters.copy()
#     won_filters.append(Project.quote_status == 'Won')
#     won_quotes = db.query(Project).filter(and_(*won_filters)).all()
#     print(f"DEBUG: all_quotes={len(all_quotes)}, won_quotes={len(won_quotes)}")
    
#     # === KPI CALCULATIONS ===
#     total_quotes = len(all_quotes)
#     total_revenue = sum(float(q.total_price or 0) for q in won_quotes)
#     avg_quote_value = sum(float(q.total_price or 0) for q in all_quotes) / total_quotes if total_quotes > 0 else 0
    
#     # Most quoted product
#     product_counts = defaultdict(int)
#     for q in all_quotes:
#         if q.product_type:
#             product_counts[q.product_type] += 1
#     most_quoted = max(product_counts.items(), key=lambda x: x[1])[0] if product_counts else 'N/A'
    
#     # Active products
#     active_products = len(set(q.product_type for q in all_quotes if q.product_type))
    
#     # === CHART 1: Product Quote Count ===
#     product_quote_counts = defaultdict(int)
#     for q in all_quotes:
#         product = q.product_type or 'Unknown'
#         product_quote_counts[product] += 1
    
#     product_quotes = [
#         {'product_type': k, 'quote_count': v}
#         for k, v in sorted(product_quote_counts.items(), key=lambda x: x[1], reverse=True)
#     ]
    
#     # === CHART 2: Revenue Contribution (Won) ===
#     product_revenue = defaultdict(float)
#     for q in won_quotes:
#         product = q.product_type or 'Unknown'
#         product_revenue[product] += float(q.total_price or 0)
    
#     revenue_contribution = [
#         {
#             'product_type': k,
#             'revenue': v,
#             'percentage': (v / total_revenue * 100) if total_revenue > 0 else 0
#         }
#         for k, v in sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
#     ]
    
#     # === CHART 3: Monthly Trend ===
#     monthly_data = defaultdict(lambda: defaultdict(int))
#     for q in all_quotes:
#         if q.quotation_date:
#             month = q.quotation_date.strftime('%Y-%m')
#             product = q.product_type or 'Unknown'
#             monthly_data[month][product] += 1
    
#     product_trend = []
#     for month in sorted(monthly_data.keys()):
#         point = {'period': month}
#         for product, count in monthly_data[month].items():
#             point[product] = count
#         product_trend.append(point)
    
#     # === CHART 4: Status Breakdown ===
#     status_data = defaultdict(lambda: {'product_type': '', 'Budgetary': 0, 'Active': 0, 'Won': 0, 'Lost': 0})
#     for q in all_quotes:
#         product = q.product_type or 'Unknown'
#         status = q.quote_status or 'Unknown'
        
#         if product not in status_data:
#             status_data[product]['product_type'] = product
        
#         if status in ['Budgetary', 'Active', 'Won', 'Lost']:
#             status_data[product][status] += 1
    
#     status_breakdown = list(status_data.values())
    
#     # === TABLE: Detailed Performance ===
#     # Global total (date filter only, no status/product/customer)
#     global_filters = []
#     if start_date and end_date:
#         global_filters.append(Project.quotation_date.between(start_date, end_date))
    
#     global_quotes = db.query(Project).filter(and_(*global_filters)).all() if global_filters else db.query(Project).all()
#     global_total = sum(float(q.total_price or 0) for q in global_quotes)
    
#     product_performance = defaultdict(lambda: {'customers': set(), 'won_revenue': 0, 'total_quoted': 0})
    
#     for q in all_quotes:
#         product = q.product_type or 'Unknown'
        
#         if q.customer_name:
#             product_performance[product]['customers'].add(q.customer_name)
        
#         if q.quote_status == 'Won':
#             product_performance[product]['won_revenue'] += float(q.total_price or 0)
        
#         product_performance[product]['total_quoted'] += float(q.total_price or 0)
    
#     detailed_performance = [
#         {
#             'product_type': product,
#             'customer_count': len(data['customers']),
#             'won_revenue': data['won_revenue'],
#             'percentage_of_total': (data['total_quoted'] / global_total * 100) if global_total > 0 else 0
#         }
#         for product, data in product_performance.items()
#     ]
#     detailed_performance.sort(key=lambda x: x['won_revenue'], reverse=True)
    
#     return {
#         'kpis': {
#             'total_quotes': {
#                 'label': 'Total Quotes',
#                 'value': total_quotes,
#                 'format_type': 'number',
#                 'change_percent': None,
#                 'change_direction': None
#             },
#             'total_revenue': {
#                 'label': 'Total Revenue (Won)',
#                 'value': total_revenue,
#                 'format_type': 'currency',
#                 'change_percent': None,
#                 'change_direction': None
#             },
#             'avg_quote_value': {
#                 'label': 'Average Quote Value',
#                 'value': avg_quote_value,
#                 'format_type': 'currency',
#                 'change_percent': None,
#                 'change_direction': None
#             },
#             'most_quoted_product': {
#                 'label': 'Most Quoted Product',
#                 'value': most_quoted,
#                 'format_type': 'text'
#             },
#             'product_count': {
#                 'label': 'Active Products',
#                 'value': active_products,
#                 'format_type': 'number'
#             }
#         },
#         'product_quotes': product_quotes,
#         'revenue_contribution': revenue_contribution,
#         'product_trend': product_trend,
#         'status_breakdown': status_breakdown,
#         'detailed_performance': detailed_performance
#     }