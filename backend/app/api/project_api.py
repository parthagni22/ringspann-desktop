"""
Project API
"""
import eel
from app.services.project_service import ProjectService
from app.database.connection import SessionLocal
from app.models.project import Project
from app.models.customer import Customer
from app.utils.logger import setup_logger

logger = setup_logger()
project_service = ProjectService()

@eel.expose
def get_recent_projects(limit=10):
    """Get recent projects"""
    try:
        projects = project_service.get_recent(limit)
        return {'success': True, 'data': projects}
    except Exception as e:
        logger.error(f"Get recent projects failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def delete_project(project_id: int):
    """Delete project permanently"""
    try:
        project_service.delete(project_id)
        return {'success': True, 'message': 'Project deleted successfully'}
    except Exception as e:
        logger.error(f"Delete project failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def get_project_by_id(project_id: int):
    """Get project details"""
    try:
        project = project_service.get_by_id(project_id)
        return {'success': True, 'data': project}
    except Exception as e:
        logger.error(f"Get project failed: {e}")
        return {'success': False, 'error': str(e)}

@eel.expose
def check_quotation_exists(quotation_number: str):
    """Check if quotation number already exists"""
    db = SessionLocal()
    try:
        exists = db.query(Project).filter(
            Project.quotation_number == quotation_number
        ).first() is not None
        return {'exists': exists}
    except Exception as e:
        logger.error(f"Check quotation exists failed: {e}")
        return {'exists': False}
    finally:
        db.close()

@eel.expose
def search_customers(search_term: str):
    """Search customers by name"""
    db = SessionLocal()
    try:
        customers = db.query(Customer).filter(
            Customer.name.ilike(f'%{search_term}%')
        ).limit(10).all()
        
        return {
            'success': True,
            'data': [{'id': c.id, 'name': c.name} for c in customers]
        }
    except Exception as e:
        logger.error(f"Search customers failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()

@eel.expose
def save_requirements(project_id: int, requirements: list):
    """Save customer requirements for project"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {'success': False, 'error': 'Project not found'}
        
        # Store requirements as JSON in project
        import json
        project.requirements_data = json.dumps(requirements)
        db.commit()
        
        return {'success': True, 'message': 'Requirements saved successfully'}
    except Exception as e:
        db.rollback()
        logger.error(f"Save requirements failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()
    """Create new project"""
    db = SessionLocal()
    try:
        # Check if quotation number exists
        exists = db.query(Project).filter(
            Project.quotation_number == quotation_number
        ).first()
        
        if exists:
            return {'success': False, 'error': 'Quotation number already exists'}
        
        # Create project
        project = Project(
            quotation_number=quotation_number,
            customer_name=customer_name,
            status='draft'
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        
        return {
            'success': True,
            'data': {
                'id': project.id,
                'quotationNo': project.quotation_number,
                'customer': project.customer_name
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Create project failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()