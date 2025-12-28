"""
Helper Functions
"""
from datetime import datetime
from typing import Optional

def format_date(date: datetime, format: str = "%Y-%m-%d") -> str:
    """Format datetime to string"""
    if not date:
        return ""
    return date.strftime(format)

def parse_date(date_str: str, format: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse string to datetime"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        return None

def generate_quotation_number() -> str:
    """Generate unique quotation number"""
    from datetime import datetime
    import random
    
    now = datetime.now()
    random_part = random.randint(1000, 9999)
    return f"Q{now.year}{now.month:02d}{now.day:02d}{random_part}"
