"""
Project Service
"""
from app.database.connection import SessionLocal
from app.models.project import Project, ProjectStatus
from datetime import datetime

class ProjectService:
    def get_recent(self, limit=10):
        """Get recent projects"""
        db = SessionLocal()
        try:
            projects = db.query(Project).order_by(
                Project.updated_at.desc()
            ).limit(limit).all()
            
            return [self._to_dict(p) for p in projects]
        finally:
            db.close()
    
    def get_by_id(self, project_id: int):
        """Get project by ID"""
        db = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise Exception("Project not found")
            return self._to_dict(project)
        finally:
            db.close()
    
    def delete(self, project_id: int):
        """Delete project permanently"""
        db = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise Exception("Project not found")
            
            db.delete(project)
            db.commit()
        finally:
            db.close()
    
    def _to_dict(self, project):
        """Convert project to dict"""
        return {
            'id': project.id,
            'name': f"{project.quotation_number}_{project.customer_name}",
            'quotationNo': project.quotation_number,
            'quotation_number': project.quotation_number,
            'customer': project.customer_name,
            'customer_name': project.customer_name,
            'requirements_data': project.requirements_data,
            'lastModified': project.updated_at.strftime('%Y-%m-%d'),
            'status': project.status.value,
            'dateCreated': project.created_at.strftime('%Y-%m-%d')
        }