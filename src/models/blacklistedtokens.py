from mongoengine import Document, StringField, DateTimeField
import datetime

class BlacklistToken(Document):
    meta = {"collection": "blacklisted_tokens"}

    token = StringField(required=True, unique=True)
    blacklisted_on = DateTimeField(default=datetime.datetime.utcnow)
