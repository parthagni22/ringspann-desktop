"""
Analytics Pydantic Models
Data models for analytics API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# REQUEST MODELS
# ============================================================================

class AnalyticsFilters(BaseModel):
    """Common filters for all analytics endpoints"""
    date_filter: str = Field(default="all", description="all | mtd | ytd | custom")
    start_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    quote_status: Optional[str] = Field("all", description="all | Budgetary | Active | Lost | Won")
    product_type: Optional[str] = Field("all", description="all | product type")
    customer: Optional[str] = Field("all", description="all | customer name")


# ============================================================================
# COMMON SUB-MODELS
# ============================================================================

class KPICard(BaseModel):
    """Standard KPI card data"""
    label: str
    value: Any
    change_percent: Optional[float] = None
    change_direction: Optional[str] = None  # "up" | "down" | "neutral"
    format_type: str = "number"  # "number" | "currency" | "percent"


class ChartDataPoint(BaseModel):
    """Generic chart data point"""
    label: str
    value: float
    metadata: Optional[Dict[str, Any]] = None


class TimeSeriesPoint(BaseModel):
    """Time series data point"""
    date: str
    value: float
    label: Optional[str] = None


class ProductData(BaseModel):
    """Product-specific data"""
    product_type: str
    quote_count: int
    revenue: float
    avg_value: float
    percentage: Optional[float] = None


class CustomerData(BaseModel):
    """Customer-specific data"""
    customer_name: str
    quote_count: int
    revenue: float
    avg_deal_size: float
    last_quote_date: Optional[str] = None


# ============================================================================
# PRODUCT ANALYTICS RESPONSE
# ============================================================================

class ProductAnalyticsResponse(BaseModel):
    """Complete product analytics response"""
    
    # KPIs
    kpis: Dict[str, KPICard]
    
    # Charts data
    quote_distribution: List[ProductData]  # Bar chart
    revenue_contribution: List[ProductData]  # Donut chart
    product_trend: List[Dict[str, Any]]  # Line chart (multi-series)
    status_breakdown: List[Dict[str, Any]]  # Stacked bar chart
    
    # Metadata
    filters_applied: Dict[str, Any]
    data_timestamp: datetime
    total_records: int


# ============================================================================
# FINANCE ANALYTICS RESPONSE
# ============================================================================

class FinanceAnalyticsResponse(BaseModel):
    """Complete finance analytics response"""
    
    # KPIs
    kpis: Dict[str, KPICard]
    
    # Charts data
    revenue_by_status: List[ChartDataPoint]  # Bar chart
    monthly_trend: List[TimeSeriesPoint]  # Line chart
    product_revenue: List[ProductData]  # Horizontal bar
    value_distribution: List[Dict[str, Any]]  # Histogram
    inquiry_timeline: List[Dict[str, Any]]  # Bar chart
    
    # Metadata
    filters_applied: Dict[str, Any]
    data_timestamp: datetime
    total_records: int


# ============================================================================
# CUSTOMER ANALYTICS RESPONSE
# ============================================================================

class CustomerAnalyticsResponse(BaseModel):
    """Complete customer analytics response"""
    
    # KPIs
    kpis: Dict[str, KPICard]
    
    # Charts data
    top_customers_by_count: List[CustomerData]  # Bar chart
    top_customers_by_revenue: List[CustomerData]  # Bar chart
    customer_status_breakdown: List[Dict[str, Any]]  # Stacked bar
    activity_timeline: List[Dict[str, Any]]  # Timeline
    new_vs_repeat: Dict[str, Any]  # Donut chart
    
    # Metadata
    filters_applied: Dict[str, Any]
    data_timestamp: datetime
    total_records: int


# ============================================================================
# COMBINED INSIGHTS RESPONSE
# ============================================================================

class CombinedInsightsResponse(BaseModel):
    """Combined insights across all views"""
    
    # Product × Customer matrix
    product_customer_matrix: Dict[str, Any]
    
    # Top combinations
    top_combinations: List[Dict[str, Any]]
    
    # Funnel data
    funnel: List[Dict[str, Any]]
    
    # Velocity data
    velocity: List[TimeSeriesPoint]
    
    # Processing time
    avg_processing_time: Optional[float]
    
    # Product mix
    product_mix_trend: List[Dict[str, Any]]
    
    # Metadata
    filters_applied: Dict[str, Any]
    data_timestamp: datetime


# ============================================================================
# EXPORT MODELS
# ============================================================================

class ExportRequest(BaseModel):
    """Request model for data export"""
    view: str  # product | finance | customer | combined
    format: str  # json | csv
    filters: AnalyticsFilters
    include_charts: bool = False


class ExportResponse(BaseModel):
    """Response model for data export"""
    success: bool
    data: Optional[Any] = None
    download_url: Optional[str] = None
    filename: str
    format: str
    generated_at: datetime


# ============================================================================
# ERROR MODELS
# ============================================================================

class AnalyticsError(BaseModel):
    """Error response model"""
    error: bool = True
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None