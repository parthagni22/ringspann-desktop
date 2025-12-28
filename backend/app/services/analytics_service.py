"""
Analytics Service
"""
import pandas as pd
from app.database.connection import SessionLocal, engine
from datetime import datetime, timedelta

class AnalyticsService:
    def get_overview(self):
        """Get overview analytics"""
        db = SessionLocal()
        try:
            # Use pandas for easy aggregation
            projects_df = pd.read_sql("SELECT * FROM projects", engine)
            
            if len(projects_df) == 0:
                return {
                    'total_projects': 0,
                    'total_customers': 0,
                    'completion_rate': 0,
                    'active_projects': 0
                }
            
            return {
                'total_projects': len(projects_df),
                'total_customers': projects_df['customer_name'].nunique(),
                'completion_rate': (projects_df['status'] == 'completed').sum() / len(projects_df) * 100,
                'active_projects': (projects_df['status'] == 'in_progress').sum()
            }
        finally:
            db.close()
    
    def get_product_analytics(self, date_filter, customer_filter):
        """Get product analytics"""
        # TODO: Implement with pandas
        return {
            'total_types': 4,
            'products': []
        }
