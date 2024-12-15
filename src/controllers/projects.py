from flask import request, jsonify , g
from src.app import app
from src.clients.auth_manager import must_be_admin, token_required
from src.controllers.decorators import json_payload_required
from src.models.projects import Project
from src.config.codingsphereslogger import logger
import datetime

BASE_PATH = "/api/v1"  # Adjust the base path as per your application

####################################################################################

@app.route(BASE_PATH + "/projects", methods=["POST"])
@token_required
@must_be_admin
@json_payload_required
def create_a_project():
    """
    Create a new project
    """
    try:
        # Get JSON payload
        data = request.get_json()

        # Validate required fields
        required_fields = ["name", "description"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Ensure project name is unique
        if Project.objects(name=data["name"]).first():
            return jsonify({"error": "A project with this name already exists"}), 409
        

        # Create a new project
        new_project = Project(
            name=data["name"],
            description=data["description"],
            user_id=g.user.get("user_id"),  # Authenticated user ID
            status=data.get("status", "active"),  # Default status is 'active'
            created_at=datetime.datetime.utcnow(),
        )

        # Save project to the database
        new_project.save()
        logger.info(f"Project created successfully: {new_project.name}")

        # Return the created project details
        return jsonify({
            "message": "Project created successfully",
            "project": {
                "project_id": str(new_project.id),
                "name": new_project.name,
                "description": new_project.description,
                "user_id": new_project.user_id,
                "status": new_project.status,
                "created_at": new_project.created_at,
                "updated_at": new_project.updated_at,
            }
        }), 201

    except Exception as e:
        print(e)
        logger.error(f"Failed to create project: {e}")
        return jsonify({"error": "Failed to create project"}), 500


@app.route(BASE_PATH + "/projects/<project_id>", methods=["GET"])
@token_required
def get_a_project(project_id):
    """
    Get project information by project ID
    """
    try:
        # Find project by ID
        project = Project.objects(id=project_id).first()

        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Return the project details
        return jsonify({
            "project": {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "user_id": project.user_id,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        }), 200

    except Exception as e:
        logger.error(f"Failed to fetch project: {e}")
        return jsonify({"error": "Failed to fetch project"}), 500


@app.route(BASE_PATH + "/projects", methods=["GET"])
@token_required
def get_projects():
    """
    Get many projects information
    """
    try:
        # Query parameters
        status = request.args.get("status")
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
        skip = (page - 1) * limit

        # Query projects based on filters
        query = Project.objects()
        if status:
            query = query.filter(status=status)

        # Pagination
        projects = query.skip(skip).limit(limit)

        # Serialize projects
        project_list = [
            {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "user_id": project.user_id,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
            for project in projects
        ]

        # Return the project list
        return jsonify({"projects": project_list, "total_count": query.count()}), 200

    except Exception as e:
        logger.error(f"Failed to fetch projects: {e}")
        return jsonify({"error": "Failed to fetch projects"}), 500


@app.route(BASE_PATH + "/projects/<project_id>", methods=["PATCH"])
@token_required
@must_be_admin
@json_payload_required
def update_a_project(project_id):
    """
    Update project information
    """
    try:
        print(project_id)
        # Get JSON payload
        data = request.get_json()

        # Find project by ID
        project = Project.objects(project_id=project_id).first()

        print(project)
        print("are u getting the project")

        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Update project fields
        for key, value in data.items():
            if hasattr(project, key) and key != "id":
                setattr(project, key, value)

        project.updated_at = datetime.datetime.utcnow()
        project.save()

        logger.info(f"Project updated successfully: {project_id}")

        # Return updated project details
        return jsonify({
            "message": "Project updated successfully",
            "project": {
                "project_id": str(project.project_id),
                "name": project.name,
                "description": project.description,
                "user_id": project.user_id,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        }), 200

    except Exception as e:
        print(e)
        logger.error(f"Failed to update project: {e}")
        return jsonify({"error": "Failed to update project"}), 500


@app.route(BASE_PATH + "/projects/<project_id>", methods=["DELETE"])
@token_required
@must_be_admin
@json_payload_required
def delete_a_project(project_id):
    """
    Delete a project by ID
    """
    try:
        # Find project by ID
        project = Project.objects(id=project_id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Delete project
        project.delete()
        logger.info(f"Project deleted successfully: {project_id}")

        return jsonify({"message": "Project deleted successfully"}), 200

    except Exception as e:
        logger.error(f"Failed to delete project: {e}")
        return jsonify({"error": "Failed to delete project"}), 500
