from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw

from enum import Enum
from mongoengine import (
    Document, StringField,
    EnumField, DateTimeField,
    ReferenceField,
)


class Status(Enum):
    ONLINE = 0
    OFFLINE = 1
    REMOVED = 2

class Device(Document):
    name = StringField(
        required=True,
    )
    apikey = StringField(
        unique=True,
        required=True
    )
    user = ReferenceField('User')
    status = EnumField(
        Status,
        default=Status.OFFLINE,
    )
    createdAt = DateTimeField(
        default=datetime.utcnow,
    )
    updatedAt = DateTimeField(
        default=datetime.utcnow,
    )

    def encrypt_apikey(self):
        if type(self.apikey) is not str:
            self.apikey = str(self.apikey)

        self.apikey = hashpw(self.apikey.encode(), gensalt(rounds=7)).decode()

    def check_apikey(self, apikey:str) -> bool:
        return checkpw(apikey.encode(), self.apikey.encode())

    def update(self, **kwargs):
        self.updatedAt = datetime.utcnow()
        kwargs['updatedAt'] = self.updatedAt
        return super().update(**kwargs)
