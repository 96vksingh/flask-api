import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, ReferenceField, ListField, QuerySet
from src.config.codingsphereslogger import logger


class ROLES:
    ADMIN = "admin"
    USER = "user"

    @staticmethod
    def __map__():
        return {x: y for x, y in vars(ROLES).items() if not x.startswith("__")}


# MongoDB Role Model
class Role(Document):
    name = StringField(required=True, max_length=50, unique_with="role_type")
    description = StringField(max_length=500)
    role_type = StringField(required=True, choices=["internal", "external"], default="external")

    # Metadata
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()

    # Validation constraints (optional)
    meta = {
        "collection": "roles",
        "indexes": ["name", "role_type"],
    }

    def save_role(self):
        self.updated_at = datetime.datetime.utcnow()
        self.save()

    @staticmethod
    def find_role_by_name_and_type(name, role_type):
        return Role.objects(name__iexact=name, role_type=role_type).first()


