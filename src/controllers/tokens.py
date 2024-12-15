from flask import request, g

from src.app import app, db

from src.clients.auth_manager import token_required
from src.controllers.decorators import json_payload_required
from src.helpers import *
from src.config.config import BASE_PATH
from src.config.codingsphereslogger import logger
from src.models.blacklistedtokens import BlacklistToken

import datetime
import jwt
from werkzeug.security import check_password_hash
from src.models.users import User  # Replace with the correct path to your User model
from src.config.config import SECRET_KEY  # Add a secret key in your config for signing JWTs



def generate_tokens(user):
    access_token_payload = {
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  # Access token expires in 15 minutes
    }

    refresh_token_payload = {
        "user_id": user.user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Refresh token expires in 7 days
    }

    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token




@app.route(BASE_PATH + "/login", methods=["POST"])
@json_payload_required
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Find user by email
        user = User.objects(email=email).first()

        if user and check_password_hash(user.password, password):
            # Generate tokens
            access_token, refresh_token = generate_tokens(user)

            # Save refresh token in the database
            user.update(refresh_token=refresh_token)

            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": "Failed to log in", "details": str(e)}), 500


@app.route(BASE_PATH +"/refresh", methods=["POST"])
@json_payload_required
def refresh_token():
    try:
        data = request.get_json()
        refresh_token = data.get("refresh_token")

        if not refresh_token:
            return jsonify({"error": "Refresh token is required"}), 400

        # Decode the refresh token
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")

        # Validate the refresh token from the database
        user = User.objects(user_id=user_id, refresh_token=refresh_token).first()
        if not user:
            return jsonify({"error": "Invalid refresh token"}), 401

        # Generate a new access token
        access_token_payload = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")

        return jsonify({"access_token": access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401
    except Exception as e:
        return jsonify({"error": "Failed to refresh token", "details": str(e)}), 500



@app.route(BASE_PATH +"/logout", methods=["POST"])
@token_required
def logout():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header is missing or invalid"}), 401

        token = auth_header.split(" ")[1]

        # Blacklist the token
        blacklisted_token = BlacklistToken(token=token)
        blacklisted_token.save()

        # Clear the refresh token for the user
        user_id = g.user.get("user_id")  # Assuming `g.user` has user info

        user = User.objects(user_id=user_id).first()

        if user:
            user.update(refresh_token=None)

        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        print(e)
        logger.error(f"Logout failed: {e}")
        return jsonify({"error": "Logout failed"}), 500