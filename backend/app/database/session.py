"""
Database Session Utilities
"""
from contextlib import contextmanager
from app.database.connection import SessionLocal

@contextmanager
def get_session():
    """Context manager for database session"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
