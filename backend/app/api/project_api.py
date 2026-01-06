import eel
from app.services.project_service import ProjectService
from app.database.connection import SessionLocal
from app.models.project import Project, QuoteStatus
from app.models.customer import Customer
from app.utils.logger import setup_logger

logger = setup_logger()
project_service = ProjectService()

# UPDATED: Get projects with pagination and search
@eel.expose
def get_projects_paginated(page=1, per_page=10, search_query=''):
    """Get projects with pagination and search"""
    db = SessionLocal()
    try:
        query = db.query(Project)
        
        # Apply search filter if provided
        if search_query and search_query.strip():
            search_term = f"%{search_query.strip()}%"
            query = query.filter(
                (Project.quotation_number.ilike(search_term)) |
                (Project.customer_name.ilike(search_term))
            )
        
        # Order by most recent first
        query = query.order_by(Project.updated_at.desc())
        
        # Get total count
        total_count = query.count()
        
        # Calculate pagination
        total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
        offset = (page - 1) * per_page
        
        # Get paginated results
        projects = query.offset(offset).limit(per_page).all()
        
        # Format results
        project_list = []
        for project in projects:
            project_list.append({
                'id': project.id,
                'quotation_number': project.quotation_number,
                'customer_name': project.customer_name,
                'status': project.status.value if project.status else 'draft',
                'quote_status': project.quote_status.value if project.quote_status else 'Budgetary',
                'created_at': project.created_at.isoformat() if project.created_at else None,
                'updated_at': project.updated_at.isoformat() if project.updated_at else None
            })
        
        return {
            'success': True,
            'data': {
                'projects': project_list,
                'current_page': page,
                'total_pages': total_pages,
                'total_count': total_count,
                'per_page': per_page
            }
        }
    except Exception as e:
        logger.error(f"Get paginated projects failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()


# NEW: Update project quote status
@eel.expose
def update_project_quote_status(project_id: int, quote_status: str):
    """Update project quote status"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {'success': False, 'error': 'Project not found'}
        
        # Validate and set status
        valid_statuses = ['Budgetary', 'Active', 'Lost', 'Won']
        if quote_status not in valid_statuses:
            return {'success': False, 'error': 'Invalid status'}
        
        # Update status
        project.quote_status = QuoteStatus[quote_status.lower()]
        db.commit()
        
        return {
            'success': True,
            'message': 'Quote status updated successfully',
            'data': {
                'id': project.id,
                'quote_status': project.quote_status.value
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Update quote status failed: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        db.close()


# EXISTING FUNCTIONS - Keep these as they are
@eel.expose
def get_recent_projects(limit=10):
    """Get recent projects - KEEP FOR BACKWARD COMPATIBILITY"""
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
def create_project(quotation_number: str, customer_name: str, quote_status: str = 'Budgetary'):
    """Create new project with quote status"""
    db = SessionLocal()
    try:
        # Check if quotation number exists
        exists = db.query(Project).filter(
            Project.quotation_number == quotation_number
        ).first()
        
        if exists:
            return {'success': False, 'error': 'Quotation number already exists'}
        
        # Validate quote status
        valid_statuses = ['Budgetary', 'Active', 'Lost', 'Won']
        if quote_status not in valid_statuses:
            quote_status = 'Budgetary'
        
        # Create project
        project = Project(
            quotation_number=quotation_number,
            customer_name=customer_name,
            status='draft',
            quote_status=QuoteStatus[quote_status.lower()]
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        
        return {
            'success': True,
            'data': {
                'id': project.id,
                'quotationNo': project.quotation_number,
                'customer': project.customer_name,
                'quote_status': project.quote_status.value if project.quote_status else 'Budgetary'
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Create project failed: {e}")
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
        
        
#---------------------------------------------        
        
        
        
        
        
        
        
        
# """
# Project API
# """
# import eel
# from app.services.project_service import ProjectService
# from app.database.connection import SessionLocal
# from app.models.project import Project
# from app.models.customer import Customer
# from app.utils.logger import setup_logger
# from app.models.technical_quotation import TechnicalQuotation
# from app.models.commercial_quotation import CommercialQuotation

# logger = setup_logger()
# project_service = ProjectService()

# @eel.expose
# def get_recent_projects(limit=10):
#     """Get recent projects"""
#     try:
#         projects = project_service.get_recent(limit)
#         return {'success': True, 'data': projects}
#     except Exception as e:
#         logger.error(f"Get recent projects failed: {e}")
#         return {'success': False, 'error': str(e)}

# @eel.expose
# def delete_project(project_id: int):
#     """Delete project permanently - CASCADE DELETE"""
#     db = SessionLocal()
#     try:
#         project = db.query(Project).filter(Project.id == project_id).first()
#         if not project:
#             raise Exception("Project not found")
        
#         # STEP 1: Delete all related technical quotations first
#         db.query(TechnicalQuotation).filter(
#             TechnicalQuotation.quotation_number == project.quotation_number
#         ).delete(synchronize_session=False)
        
#         # STEP 2: Delete all related commercial quotations
#         db.query(CommercialQuotation).filter(
#             CommercialQuotation.quotation_number == project.quotation_number
#         ).delete(synchronize_session=False)
        
#         # STEP 3: Now delete the project
#         db.delete(project)
#         db.commit()
        
#         return {'success': True, 'message': 'Project and all related quotations deleted'}
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Delete project failed: {e}")
#         return {'success': False, 'error': str(e)}
#     finally:
#         db.close()

# @eel.expose
# def get_project_by_id(project_id: int):
#     """Get project details"""
#     try:
#         project = project_service.get_by_id(project_id)
#         return {'success': True, 'data': project}
#     except Exception as e:
#         logger.error(f"Get project failed: {e}")
#         return {'success': False, 'error': str(e)}

# @eel.expose
# def check_quotation_exists(quotation_number: str):
#     """Check if quotation number already exists"""
#     db = SessionLocal()
#     try:
#         exists = db.query(Project).filter(
#             Project.quotation_number == quotation_number
#         ).first() is not None
#         return {'exists': exists}
#     except Exception as e:
#         logger.error(f"Check quotation exists failed: {e}")
#         return {'exists': False}
#     finally:
#         db.close()

# @eel.expose
# def search_customers(search_term: str):
#     """Search customers by name"""
#     db = SessionLocal()
#     try:
#         customers = db.query(Customer).filter(
#             Customer.name.ilike(f'%{search_term}%')
#         ).limit(10).all()
        
#         return {
#             'success': True,
#             'data': [{'id': c.id, 'name': c.name} for c in customers]
#         }
#     except Exception as e:
#         logger.error(f"Search customers failed: {e}")
#         return {'success': False, 'error': str(e)}
#     finally:
#         db.close()
        
        
# @eel.expose
# def create_project(quotation_number: str, customer_name: str):
#     """Create new project"""
#     db = SessionLocal()
#     try:
#         # Check if quotation number exists
#         exists = db.query(Project).filter(
#             Project.quotation_number == quotation_number
#         ).first()
        
#         if exists:
#             return {'success': False, 'error': 'Quotation number already exists'}
        
#         # Create project
#         project = Project(
#             quotation_number=quotation_number,
#             customer_name=customer_name,
#             status='draft'
#         )
#         db.add(project)
#         db.commit()
#         db.refresh(project)
        
#         return {
#             'success': True,
#             'data': {
#                 'id': project.id,
#                 'quotationNo': project.quotation_number,
#                 'customer': project.customer_name
#             }
#         }
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Create project failed: {e}")
#         return {'success': False, 'error': str(e)}
#     finally:
#         db.close()        

# @eel.expose
# def save_requirements(project_id: int, requirements: list):
#     """Save customer requirements for project"""
#     db = SessionLocal()
#     try:
#         project = db.query(Project).filter(Project.id == project_id).first()
#         if not project:
#             return {'success': False, 'error': 'Project not found'}
        
#         # Store requirements as JSON in project
#         import json
#         project.requirements_data = json.dumps(requirements)
#         db.commit()
        
#         return {'success': True, 'message': 'Requirements saved successfully'}
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Save requirements failed: {e}")
#         return {'success': False, 'error': str(e)}
#     finally:
#         db.close()
#     """Create new project"""
#     db = SessionLocal()
#     try:
#         # Check if quotation number exists
#         exists = db.query(Project).filter(
#             Project.quotation_number == quotation_number
#         ).first()
        
#         if exists:
#             return {'success': False, 'error': 'Quotation number already exists'}
        
#         # Create project
#         project = Project(
#             quotation_number=quotation_number,
#             customer_name=customer_name,
#             status='draft'
#         )
#         db.add(project)
#         db.commit()
#         db.refresh(project)
        
#         return {
#             'success': True,
#             'data': {
#                 'id': project.id,
#                 'quotationNo': project.quotation_number,
#                 'customer': project.customer_name
#             }
#         }
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Create project failed: {e}")
#         return {'success': False, 'error': str(e)}
#     finally:
#         db.close()