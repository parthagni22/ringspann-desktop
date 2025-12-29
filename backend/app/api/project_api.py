"""
Project API
"""
import eel
from app.services.project_service import ProjectService
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