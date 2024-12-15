import datetime
import uuid
from mongoengine import Document, StringField, DateTimeField, ReferenceField, CASCADE, BooleanField

class Project(Document):
    meta = {
        "collection": "projects",  # Name of the collection in MongoDB
        "indexes": [
            {"fields": ["name"], "unique": True},  # Ensures project names are unique
        ],
    }

    # Fields
    project_id = StringField(primary_key=True, default=lambda: uuid.uuid4().hex)  # Unique ID for the project
    name = StringField(required=True, max_length=255, unique=True)  # Project name
    description = StringField(max_length=1000)  # Description of the project
    user_id = StringField(required=True)  # ID of the user who added the project
    status = StringField(default="active", choices=["active", "inactive", "archived"])  # Status of the project
    created_at = DateTimeField(default=datetime.datetime.utcnow)  # Timestamp when created
    updated_at = DateTimeField()  # Timestamp when last updated

    def save_project(self):
        """
        Save the project and update the `updated_at` timestamp.
        """
        self.updated_at = datetime.datetime.utcnow()
        self.save()

    @staticmethod
    def create_project(data):
        """
        Create a new project in MongoDB.
        :param data: Dictionary containing project details.
        """
        try:
            new_project = Project(
                name=data.get("name"),
                description=data.get("description"),
                user_id=data.get("user_id"),
                status=data.get("status", "active"),  # Default status is 'active'
            )
            new_project.save_project()
            return {"message": "Project created successfully", "project_id": new_project.project_id}
        except Exception as e:
            return {"error": f"Failed to create project: {e}"}

    @staticmethod
    def get_projects(user_id=None, status=None, page=1, offset=20):
        """
        Get projects with optional filters (by user_id and/or status) and pagination.
        """
        query = Project.objects()
        if user_id:
            query = query.filter(user_id=user_id)
        if status:
            query = query.filter(status=status)

        projects = query.skip((page - 1) * offset).limit(offset)
        return [
            {
                "project_id": project.project_id,
                "name": project.name,
                "description": project.description,
                "user_id": project.user_id,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
            for project in projects
        ]

    @staticmethod
    def update_project(project_id, data):
        """
        Update a project by project_id.
        :param project_id: ID of the project to update.
        :param data: Dictionary of fields to update.
        """
        try:
            project = Project.objects(project_id=project_id).first()
            if not project:
                return {"error": "Project not found"}

            # Update the fields
            for key, value in data.items():
                if hasattr(project, key):
                    setattr(project, key, value)

            project.save_project()
            return {"message": "Project updated successfully"}
        except Exception as e:
            return {"error": f"Failed to update project: {e}"}

    @staticmethod
    def delete_project(project_id):
        """
        Delete a project by project_id.
        :param project_id: ID of the project to delete.
        """
        try:
            project = Project.objects(project_id=project_id).first()
            if not project:
                return {"error": "Project not found"}

            project.delete()
            return {"message": "Project deleted successfully"}
        except Exception as e:
            return {"error": f"Failed to delete project: {e}"}
