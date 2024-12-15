from flask import request, jsonify
from src.app import app
from src.clients.auth_manager import must_be_admin, token_required
from src.controllers.decorators import json_payload_required
from src.models.users import User
from src.models.roles import ROLES
from src.config.codingsphereslogger import logger
from werkzeug.security import generate_password_hash


import datetime
import jwt
# from werkzeug.security import check_password_hash
BASE_PATH = "/api/v1"  # Adjust the base path as per your application

####################################################################################

@app.route(BASE_PATH + "/users", methods=["POST"])
@token_required
# @must_be_admin
@json_payload_required
def create_a_user():
    """
    Create a new user
    """
    try:
        # Get JSON payload
        data = request.get_json()

        # Validate required fields
        required_fields = ["first_name", "email", "password", "role"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Validate role
        role = data["role"]
        if role not in ROLES.__map__().values():
            return jsonify({"error": f"Invalid role: {role}"}), 400

        # Check if the email already exists
        if User.objects(email=data["email"].lower()).first():
            return jsonify({"error": "A user with this email already exists"}), 409

        # Hash the password
        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

        # Create a new user
        new_user = User(
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            email=data["email"].lower(),
            phone=data.get("phone"),
            password=hashed_password,
            role=role,  # Assign the role
            status=data.get("status", "active"),
            created_at=datetime.datetime.utcnow(),
        )

        # Save user to the database
        new_user.save()
        logger.info(f"User created successfully: {new_user.email}")

        # Return the created user details
        return jsonify({
            "message": "User created successfully",
            "user": {
                "id": str(new_user.id),
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "role": new_user.role,
                "status": new_user.status,
                "created_at": new_user.created_at
            }
        }), 201

    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        return jsonify({"error": "Failed to create user"}), 500


@app.route(BASE_PATH + "/users/<user_id>", methods=["GET"])
@token_required
def get_a_user(user_id):
    """
    Get user information by user ID
    """
    try:
        # Find user by ID
        user = User.objects(id=user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Return the user details
        return jsonify({
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        }), 200

    except Exception as e:
        logger.error(f"Failed to fetch user: {e}")
        return jsonify({"error": "Failed to fetch user"}), 500


@app.route(BASE_PATH + "/users", methods=["GET"])
@token_required
@must_be_admin
def get_users():
    """
    Get many users information
    """
    try:
        # Query parameters
        status = request.args.get("status")
        role = request.args.get("role")
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
        skip = (page - 1) * limit

        # Query users based on filters
        query = User.objects()
        if status:
            query = query.filter(status=status)
        if role:
            query = query.filter(role=role)

        # Pagination
        users = query.skip(skip).limit(limit)

        # Serialize users
        user_list = [
            {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in users
        ]

        # Return the user list
        return jsonify({"users": user_list, "total_count": query.count()}), 200

    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        return jsonify({"error": "Failed to fetch users"}), 500


@app.route(BASE_PATH + "/users/<user_id>", methods=["DELETE"])
@token_required
@must_be_admin
def delete_a_user(user_id):
    """
    Delete a user by ID
    """
    try:
        # Find user by ID
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete user
        user.delete()
        logger.info(f"User deleted successfully: {user_id}")

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        logger.error(f"Failed to delete user: {e}")
        return jsonify({"error": "Failed to delete user"}), 500


@app.route(BASE_PATH + "/users/<user_id>", methods=["PATCH"])
@token_required
@must_be_admin
@json_payload_required
def update_a_user(user_id):
    """
    Update user information
    """
    try:
        # Get JSON payload
        data = request.get_json()

        # Find user by ID
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user fields
        for key, value in data.items():
            if hasattr(user, key) and key != "id":
                setattr(user, key, value)

        user.updated_at = datetime.datetime.utcnow()
        user.save()

        logger.info(f"User updated successfully: {user_id}")

        # Return updated user details
        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        }), 200

    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        return jsonify({"error": "Failed to update user"}), 500

