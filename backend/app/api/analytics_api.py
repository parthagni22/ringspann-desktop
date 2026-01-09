"""
Analytics API endpoints for Eel Desktop Application
Maps analytics routes to Eel-exposed functions
"""
#from django import db
import eel
from typing import Optional
from datetime import datetime
from app.database.connection import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.models.analytics_models import AnalyticsFilters
from app.utils.logger import setup_logger
import json


logger = setup_logger()


# ============================================================================
# PRODUCT ANALYTICS
# ============================================================================

@eel.expose
def get_product_analytics(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: str = "all",
    customer: str = "all",
    product_type: str = "all"
):
    """Get complete product analytics"""
    try:
        db = SessionLocal()  # ← ADD THIS
        
        from app.services.product_analytics_service import get_product_analytics_updated
        
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date,
            quote_status=quote_status,
            customer=customer,
            product_type=product_type
        )
        
        result = get_product_analytics_updated(db, filters)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_product_analytics: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@eel.expose
def get_quotes_by_product(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: str = "all"
):
    """Get quotes count by product type"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date,
            quote_status=quote_status
        )
        
        service = AnalyticsService(db)
        result = service.get_quotes_by_product(filters)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_quotes_by_product: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# FINANCE ANALYTICS
# ============================================================================

@eel.expose
def get_finance_analytics(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: str = "all",
    product_type: str = "all",
    customer: str = "all"
):
    """Get complete finance analytics"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date,
            quote_status=quote_status,
            product_type=product_type,
            customer=customer
        )
        
        service = AnalyticsService(db)
        result = service.get_finance_analytics(filters)
        
        db.close()
        
        # Debug: Check what result looks like
        logger.info(f"Finance result type: {type(result)}")
        logger.info(f"Finance result: {result}")
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        import traceback
        logger.error(f"Error in get_finance_analytics: {e}")
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "error": str(e)
        }


@eel.expose
def get_revenue_by_status(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get revenue breakdown by quote status"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        service = AnalyticsService(db)
        result = service.get_revenue_by_status(filters)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_revenue_by_status: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@eel.expose
def get_monthly_revenue_trend(
    months: int = 12,
    quote_status: str = "all"
):
    """Get monthly revenue trend"""
    try:
        db = SessionLocal()
        service = AnalyticsService(db)
        result = service.get_monthly_revenue_trend(months, quote_status)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_monthly_revenue_trend: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# CUSTOMER ANALYTICS
# ============================================================================

@eel.expose
def get_customer_analytics(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    quote_status: str = "all",
    product_type: str = "all"
):
    """Get complete customer analytics"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date,
            quote_status=quote_status,
            product_type=product_type
        )
        
        service = AnalyticsService(db)
        result = service.get_customer_analytics(filters)
        
        db.close()
        
        return {
            "success": True,
            "data": result.model_dump()
        }
    except Exception as e:
        logger.error(f"Error in get_customer_analytics: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@eel.expose
def get_top_customers(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sort_by: str = "revenue",
    limit: int = 10
):
    """Get top customers by revenue or quote count"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        service = AnalyticsService(db)
        result = service.get_top_customers(filters, sort_by, limit)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_top_customers: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# COMBINED INSIGHTS
# ============================================================================

@eel.expose
def get_combined_insights(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get combined insights across all views"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        service = AnalyticsService(db)
        result = service.get_combined_insights(filters)
        
        db.close()
        
        return {
            "success": True,
            "data": result.model_dump()
        }
    except Exception as e:
        logger.error(f"Error in get_combined_insights: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@eel.expose
def get_product_customer_matrix(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: str = "quote_count"
):
    """Get product × customer matrix"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        service = AnalyticsService(db)
        result = service.get_product_customer_matrix(filters, metric)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_product_customer_matrix: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@eel.expose
def get_quote_status_funnel(
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get quote status funnel"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        service = AnalyticsService(db)
        result = service.get_quote_status_funnel(filters)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_quote_status_funnel: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@eel.expose
def get_quote_velocity(months: int = 12):
    """Get monthly quote velocity"""
    try:
        db = SessionLocal()
        service = AnalyticsService(db)
        result = service.get_quote_velocity(months)
        
        db.close()
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_quote_velocity: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# EXPORT FUNCTIONALITY
# ============================================================================

@eel.expose
def export_analytics_data(
    view: str,
    format: str = "json",
    date_filter: str = "all",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Export analytics data"""
    try:
        db = SessionLocal()
        filters = AnalyticsFilters(
            date_filter=date_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        service = AnalyticsService(db)
        result = service.export_analytics_data(view, format, filters)
        
        db.close()
        
        return result
    except Exception as e:
        logger.error(f"Error in export_analytics_data: {e}")
        return {
            "success": False,
            "error": str(e)
        }


logger.info("Analytics API endpoints registered")

@eel.expose
def get_customers_for_analytics():
    """Get all unique customers for filter dropdown"""
    try:
        db = SessionLocal()
        from app.models.project import Project
        
        customers = db.query(Project.customer_name).distinct().all()
        customer_list = [{"customer_name": c[0]} for c in customers if c[0]]
        
        db.close()
        
        return {
            "success": True,
            "data": customer_list
        }
    except Exception as e:
        logger.error(f"Error in get_customers_for_analytics: {e}")
        return {
            "success": False,
            "error": str(e)
        }






















# """
# Analytics API
# """
# import eel
# from app.services.analytics_service import AnalyticsService
# from app.utils.logger import setup_logger

# logger = setup_logger()
# analytics_service = AnalyticsService()

# @eel.expose
# def get_overview_analytics():
#     """Get overview analytics"""
#     try:
#         data = analytics_service.get_overview()
#         return {'success': True, 'data': data}
#     except Exception as e:
#         logger.error(f"Get overview analytics failed: {e}")
#         return {'success': False, 'error': str(e)}

# @eel.expose
# def get_product_analytics(date_filter='all', customer_filter='All'):
#     """Get product analytics"""
#     try:
#         data = analytics_service.get_product_analytics(date_filter, customer_filter)
#         return {'success': True, 'data': data}
#     except Exception as e:
#         logger.error(f"Get product analytics failed: {e}")
#         return {'success': False, 'error': str(e)}
