import sys
import ujson
from functools import wraps
from flask import request, Response, g

from src.config.config import *
from src.models.blacklistedtokens import BlacklistToken
from src.models.users import User
from src.models.roles import ROLES

from src.config.codingsphereslogger import logger

from src.helpers import *

from flask import request, jsonify
import jwt
from functools import wraps
from src.config.config import SECRET_KEY  # Secret key for signing JWT


def error_response(msg, code):
  """
  Return 304 response for auth failure

  :param  msg: [string or array] e.g. "user not found"
  :param  code: [string] e.g. USER_NOT_FOUND

  :return [Object] Response object
  """
  return Response(
    response=ujson.dumps({"errors": msg, "code": code}),
    status=403,
    mimetype="application/json"
  )


from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.error("Authorization header is missing")
            return jsonify({"error": "Authorization header is missing"}), 401

        # Check if the token starts with "Bearer"
        if not auth_header.startswith("Bearer "):
            logger.error("Invalid token format: missing 'Bearer ' prefix")
            return jsonify({"error": "Invalid token format"}), 401

        # Remove "Bearer " from the token
        token = auth_header.split(" ")[1]
        try:
            if BlacklistToken.objects(token=token).first():
                return jsonify({"error": "Token has been invalidated"}), 401

            # Decode the token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token  # Attach user info to request for use in the route
            # print(decoded_token)
            # users = User.query.filter_by(email=decoded_token['email'])
            user = User.objects(email__iexact=decoded_token['email']).first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Serialize the user data
            user_data = {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "work_title": user.work_title,
                "status": user.status,
                "profile_image_url": user.profile_image_url,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            # print(user_data)
            g.user = decoded_token
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

def must_be_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("i came here to check admin")
        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.error("Authorization header is missing")
            return jsonify({"error": "Authorization header is missing"}), 401

        # Check token format
        if not auth_header.startswith("Bearer "):
            logger.error("Invalid token format: missing 'Bearer ' prefix")
            return jsonify({"error": "Invalid token format"}), 401

        # Extract the token
        token = auth_header.split(" ")[1]
        try:
            # Decode the token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            email = decoded_token.get("email")
            if not email:
                logger.error("Token does not contain email")
                return jsonify({"error": "Invalid token: Missing email"}), 401

            # Fetch the user from the database
            user = User.objects(email__iexact=email).first()
            if not user:
                logger.error(f"User not found: {email}")
                return jsonify({"error": "User not found"}), 404

            # Check if the user has the "admin" role
            if user.role != ROLES.ADMIN:  # Assuming `role` is a single Role object
                logger.error(f"Unauthorized access: User {email} is not an admin")
                return jsonify({"error": "You must be an admin to access this resource"}), 403

            # Attach user information to the Flask global object
            g.user = {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
            }

        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return jsonify({"error": "Something went wrong"}), 500

        # If all checks pass, proceed to the route
        return f(*args, **kwargs)

    return decorated


