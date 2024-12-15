import datetime
import secrets
import uuid
from mongoengine import (
    Document,
    StringField,
    EmailField,
    DateTimeField,
    ReferenceField,
    CASCADE,
    QuerySet,
)
from src.config.codingsphereslogger import logger


class ROLES:
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    INSTALLER = "installer"
    STAFF = "staff"
    USER = "user"
    WAREHOUSESCANNER = "warehousescanner"

    @staticmethod
    def __map__():
        return {x: y for x, y in vars(ROLES).items() if not x.startswith("__")}


class User(Document):
    meta = {
        "collection": "users",
        "indexes": [
            {"fields": ["email"], "unique": True},
        ],
    }

    # Fields
    user_id = StringField(primary_key=True, default=lambda: uuid.uuid4().hex)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(max_length=50)
    phone = StringField(max_length=20)
    email = EmailField(required=True, unique=True)
    work_title = StringField(max_length=100)
    password = StringField(required=True)
    status = StringField(default="active", choices=["active", "inactive", "pending"])
    profile_image_url = StringField(max_length=400)

    # Role field
    role = StringField(required=True, choices=list(ROLES.__map__().values()))

    # Refresh token field
    refresh_token = StringField()  # Field to store the refresh token

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()
    last_login_date_time = DateTimeField()

    # Save user and update timestamps
    def save_user(self):
        self.updated_at = datetime.datetime.utcnow()
        self.save()

    @staticmethod
    def create_a_user(data):
        """
        Create a new user in MongoDB
        """
        try:
            # Validate role
            role = data.get("role", ROLES.USER)  # Default role is 'user'
            if role not in ROLES.__map__().values():
                return {"error": f"Invalid role: {role}"}

            # Create the new user
            new_user = User(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone=data.get("phone"),
                email=data.get("email").lower(),
                work_title=data.get("work_title"),
                password=secrets.token_urlsafe(10),  # Temporary password
                role=role,
            )

            new_user.save_user()

            return {"message": "User created successfully", "user_id": new_user.user_id}
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return {"error": "Failed to create user"}

    @staticmethod
    def get_users(page=1, offset=20, status=None, role=None):
        """
        Get users with optional filters and pagination
        """
        query = User.objects()
        if status:
            query = query.filter(status=status)
        if role:
            query = query.filter(role=role)

        users = query.skip((page - 1) * offset).limit(offset)
        return [
            {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "status": user.status,
                "role": user.role,
                "refresh_token": user.refresh_token,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in users
        ]

    @staticmethod
    def delete_a_user(user_id):
        """
        Delete a user by user_id
        """
        user = User.objects(user_id=user_id).first()
        if not user:
            return {"error": "User not found"}
        user.delete()
        return {"message": "User deleted successfully"}

    @staticmethod
    def get_user_by_email(email):
        """
        Fetch a user by email
        """
        user = User.objects(email__iexact=email).first()
        if not user:
            return {"error": "User not found"}
        return {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "status": user.status,
            "role": user.role,
            "refresh_token": user.refresh_token,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    @staticmethod
    def update_refresh_token(user_id, refresh_token):
        """
        Update the refresh token for a user
        """
        user = User.objects(user_id=user_id).first()
        if not user:
            return {"error": "User not found"}
        user.refresh_token = refresh_token
        user.save_user()
        return {"message": "Refresh token updated successfully"}
