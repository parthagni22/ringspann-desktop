"""
Analytics API Routes
Handles all analytics endpoints for Product, Finance, Customer, and Combined views
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService
from app.models.analytics_models import (
    AnalyticsFilters,
    ProductAnalyticsResponse,
    FinanceAnalyticsResponse,
    CustomerAnalyticsResponse,
    CombinedInsightsResponse
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ============================================================================
# PRODUCT ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/products/summary", response_model=ProductAnalyticsResponse)
async def get_product_analytics_summary(
    date_filter: Optional[str] = Query("all", enum=["all", "mtd", "ytd", "custom"]),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: Optional[str] = Query("all"),
    customer: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """
    Get complete product analytics including KPIs and charts data
    
    Filters:
    - date_filter: all | mtd | ytd | custom
    - start_date: YYYY-MM-DD (required if date_filter=custom)
    - end_date: YYYY-MM-DD (required if date_filter=custom)
    - quote_status: all | Budgetary | Active | Lost | Won
    - customer: all | [customer_name]
    """
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date,
        quote_status=quote_status,
        customer=customer
    )
    
    service = AnalyticsService(db)
    return service.get_product_analytics(filters)


@router.get("/products/quotes-by-product")
async def get_quotes_by_product(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """Get quote count and distribution by product type"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date,
        quote_status=quote_status
    )
    
    service = AnalyticsService(db)
    return service.get_quotes_by_product(filters)


@router.get("/products/revenue-by-product")
async def get_revenue_by_product(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """Get revenue breakdown by product type"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date,
        quote_status=quote_status
    )
    
    service = AnalyticsService(db)
    return service.get_revenue_by_product(filters)


@router.get("/products/trend")
async def get_product_trend(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    product_type: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """Get product quotes trend over time"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date,
        product_type=product_type
    )
    
    service = AnalyticsService(db)
    return service.get_product_trend(filters)


# ============================================================================
# FINANCE ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/finance/summary", response_model=FinanceAnalyticsResponse)
async def get_finance_analytics_summary(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: Optional[str] = Query("all"),
    product_type: Optional[str] = Query("all"),
    customer: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """
    Get complete finance analytics including KPIs and charts data
    """
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date,
        quote_status=quote_status,
        product_type=product_type,
        customer=customer
    )
    
    service = AnalyticsService(db)
    return service.get_finance_analytics(filters)


@router.get("/finance/revenue-by-status")
async def get_revenue_by_status(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get revenue breakdown by quote status"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_revenue_by_status(filters)


@router.get("/finance/monthly-trend")
async def get_monthly_revenue_trend(
    months: Optional[int] = Query(12, ge=1, le=24),
    quote_status: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """Get monthly revenue trend for last N months"""
    service = AnalyticsService(db)
    return service.get_monthly_revenue_trend(months, quote_status)


@router.get("/finance/quote-value-distribution")
async def get_quote_value_distribution(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get distribution of quote values (histogram data)"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_quote_value_distribution(filters)


# ============================================================================
# CUSTOMER ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/customers/summary", response_model=CustomerAnalyticsResponse)
async def get_customer_analytics_summary(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: Optional[str] = Query("all"),
    product_type: Optional[str] = Query("all"),
    db: Session = Depends(get_db)
):
    """
    Get complete customer analytics including KPIs and charts data
    """
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date,
        quote_status=quote_status,
        product_type=product_type
    )
    
    service = AnalyticsService(db)
    return service.get_customer_analytics(filters)


@router.get("/customers/top-customers")
async def get_top_customers(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sort_by: Optional[str] = Query("revenue", enum=["revenue", "quote_count"]),
    limit: Optional[int] = Query(10, ge=5, le=50),
    db: Session = Depends(get_db)
):
    """Get top customers by revenue or quote count"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_top_customers(filters, sort_by, limit)


@router.get("/customers/status-breakdown")
async def get_customer_status_breakdown(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = Query(10),
    db: Session = Depends(get_db)
):
    """Get quote status breakdown per customer"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_customer_status_breakdown(filters, limit)


@router.get("/customers/activity-timeline")
async def get_customer_activity_timeline(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get customer activity timeline"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_customer_activity_timeline(filters)


# ============================================================================
# COMBINED INSIGHTS ENDPOINTS
# ============================================================================

@router.get("/insights/summary", response_model=CombinedInsightsResponse)
async def get_combined_insights_summary(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get combined insights across products, customers, and finance
    """
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_combined_insights(filters)


@router.get("/insights/product-customer-matrix")
async def get_product_customer_matrix(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = Query("quote_count", enum=["quote_count", "revenue"]),
    db: Session = Depends(get_db)
):
    """Get product × customer matrix (heatmap data)"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_product_customer_matrix(filters, metric)


@router.get("/insights/funnel")
async def get_quote_status_funnel(
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get quote status funnel data"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.get_quote_status_funnel(filters)


@router.get("/insights/velocity")
async def get_quote_velocity(
    months: Optional[int] = Query(12, ge=3, le=24),
    db: Session = Depends(get_db)
):
    """Get monthly quote velocity (quotes created per month)"""
    service = AnalyticsService(db)
    return service.get_quote_velocity(months)


# ============================================================================
# EXPORT ENDPOINTS
# ============================================================================

@router.get("/export/data")
async def export_analytics_data(
    view: str = Query(..., enum=["product", "finance", "customer", "combined"]),
    format: str = Query("json", enum=["json", "csv"]),
    date_filter: Optional[str] = Query("all"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export analytics data in JSON or CSV format"""
    filters = AnalyticsFilters(
        date_filter=date_filter,
        start_date=start_date,
        end_date=end_date
    )
    
    service = AnalyticsService(db)
    return service.export_analytics_data(view, format, filters)