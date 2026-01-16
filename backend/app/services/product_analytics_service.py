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


