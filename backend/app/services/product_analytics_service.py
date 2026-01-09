"""
Product Analytics Service - Updated Requirements
Separate file to avoid breaking existing analytics_service.py
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict


def get_date_range(date_filter: str, start_date: Optional[str], end_date: Optional[str]):
    """Helper to get date range filter"""
    today = datetime.now().date()
    
    if date_filter == 'week':
        return today - timedelta(days=7), today
    elif date_filter == 'month':
        return today - timedelta(days=30), today
    elif date_filter == 'quarter':
        return today - timedelta(days=90), today
    elif date_filter == 'year':
        return today - timedelta(days=365), today
    elif date_filter == 'custom' and start_date and end_date:
        return datetime.strptime(start_date, '%Y-%m-%d').date(), datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        return None, None


def get_product_analytics_updated(db: Session, filters):
    """
    Updated product analytics with new requirements:
    1. Total Revenue = Won quotes only
    2. Avg Quote Value = all quotes formula
    3. Product quotes count (all statuses)
    4. Revenue contribution (Won only)
    5. Table: Customer count, Won revenue, % of total
    """
    from app.models.project import Project
    
    # Build base query
    query_filters = []
    
    # Date filter
    start_date, end_date = get_date_range(filters.date_filter, filters.start_date, filters.end_date)
    if start_date and end_date:
        query_filters.append(Project.quotation_date.between(start_date, end_date))
    
    # Status filter
    if filters.quote_status and filters.quote_status != 'all':
        query_filters.append(Project.quote_status == filters.quote_status)
    
    # Product Type filter
    if filters.product_type and filters.product_type != 'all':
        query_filters.append(Project.product_type == filters.product_type)
    
    # Customer filter
    if filters.customer and filters.customer != 'all':
        query_filters.append(Project.customer_name == filters.customer)
    
    # Get all quotes matching filters
    all_quotes = db.query(Project).filter(and_(*query_filters)).all() if query_filters else db.query(Project).all()
    
    # Get won quotes only
    won_filters = query_filters.copy()
    won_filters.append(Project.quote_status == 'Won')
    won_quotes = db.query(Project).filter(and_(*won_filters)).all()
    print(f"DEBUG: all_quotes={len(all_quotes)}, won_quotes={len(won_quotes)}")
    
    # === KPI CALCULATIONS ===
    total_quotes = len(all_quotes)
    total_revenue = sum(float(q.total_price or 0) for q in won_quotes)
    avg_quote_value = sum(float(q.total_price or 0) for q in all_quotes) / total_quotes if total_quotes > 0 else 0
    
    # Most quoted product
    product_counts = defaultdict(int)
    for q in all_quotes:
        if q.product_type:
            product_counts[q.product_type] += 1
    most_quoted = max(product_counts.items(), key=lambda x: x[1])[0] if product_counts else 'N/A'
    
    # Active products
    active_products = len(set(q.product_type for q in all_quotes if q.product_type))
    
    # === CHART 1: Product Quote Count ===
    product_quote_counts = defaultdict(int)
    for q in all_quotes:
        product = q.product_type or 'Unknown'
        product_quote_counts[product] += 1
    
    product_quotes = [
        {'product_type': k, 'quote_count': v}
        for k, v in sorted(product_quote_counts.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # === CHART 2: Revenue Contribution (Won) ===
    product_revenue = defaultdict(float)
    for q in won_quotes:
        product = q.product_type or 'Unknown'
        product_revenue[product] += float(q.total_price or 0)
    
    revenue_contribution = [
        {
            'product_type': k,
            'revenue': v,
            'percentage': (v / total_revenue * 100) if total_revenue > 0 else 0
        }
        for k, v in sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # === CHART 3: Monthly Trend ===
    monthly_data = defaultdict(lambda: defaultdict(int))
    for q in all_quotes:
        if q.quotation_date:
            month = q.quotation_date.strftime('%Y-%m')
            product = q.product_type or 'Unknown'
            monthly_data[month][product] += 1
    
    product_trend = []
    for month in sorted(monthly_data.keys()):
        point = {'period': month}
        for product, count in monthly_data[month].items():
            point[product] = count
        product_trend.append(point)
    
    # === CHART 4: Status Breakdown ===
    status_data = defaultdict(lambda: {'product_type': '', 'Budgetary': 0, 'Active': 0, 'Won': 0, 'Lost': 0})
    for q in all_quotes:
        product = q.product_type or 'Unknown'
        status = q.quote_status or 'Unknown'
        
        if product not in status_data:
            status_data[product]['product_type'] = product
        
        if status in ['Budgetary', 'Active', 'Won', 'Lost']:
            status_data[product][status] += 1
    
    status_breakdown = list(status_data.values())
    
    # === TABLE: Detailed Performance ===
    # Global total (date filter only, no status/product/customer)
    global_filters = []
    if start_date and end_date:
        global_filters.append(Project.quotation_date.between(start_date, end_date))
    
    global_quotes = db.query(Project).filter(and_(*global_filters)).all() if global_filters else db.query(Project).all()
    global_total = sum(float(q.total_price or 0) for q in global_quotes)
    
    product_performance = defaultdict(lambda: {'customers': set(), 'won_revenue': 0, 'total_quoted': 0})
    
    for q in all_quotes:
        product = q.product_type or 'Unknown'
        
        if q.customer_name:
            product_performance[product]['customers'].add(q.customer_name)
        
        if q.quote_status == 'Won':
            product_performance[product]['won_revenue'] += float(q.total_price or 0)
        
        product_performance[product]['total_quoted'] += float(q.total_price or 0)
    
    detailed_performance = [
        {
            'product_type': product,
            'customer_count': len(data['customers']),
            'won_revenue': data['won_revenue'],
            'percentage_of_total': (data['total_quoted'] / global_total * 100) if global_total > 0 else 0
        }
        for product, data in product_performance.items()
    ]
    detailed_performance.sort(key=lambda x: x['won_revenue'], reverse=True)
    
    return {
        'kpis': {
            'total_quotes': {
                'label': 'Total Quotes',
                'value': total_quotes,
                'format_type': 'number',
                'change_percent': None,
                'change_direction': None
            },
            'total_revenue': {
                'label': 'Total Revenue (Won)',
                'value': total_revenue,
                'format_type': 'currency',
                'change_percent': None,
                'change_direction': None
            },
            'avg_quote_value': {
                'label': 'Average Quote Value',
                'value': avg_quote_value,
                'format_type': 'currency',
                'change_percent': None,
                'change_direction': None
            },
            'most_quoted_product': {
                'label': 'Most Quoted Product',
                'value': most_quoted,
                'format_type': 'text'
            },
            'product_count': {
                'label': 'Active Products',
                'value': active_products,
                'format_type': 'number'
            }
        },
        'product_quotes': product_quotes,
        'revenue_contribution': revenue_contribution,
        'product_trend': product_trend,
        'status_breakdown': status_breakdown,
        'detailed_performance': detailed_performance
    }