from datetime import datetime

from enum import Enum
from mongoengine import (
    Document, StringField,
    EnumField, DateTimeField,
    ReferenceField,
)


class Type(Enum):
    INPUT = 0
    OUTPUT = 1
    BOTH = 2

class Sensor(Document):
    name = StringField(
        required=True,
    )
    device = ReferenceField('Device')
    type = EnumField(
        Type,
        default=Type.BOTH,
    )
    createdAt = DateTimeField(
        default=datetime.utcnow,
    )
    updatedAt = DateTimeField(
        default=datetime.utcnow,
    )

    def update(self, **kwargs):
        self.updatedAt = datetime.utcnow()
        kwargs['updatedAt'] = self.updatedAt
        return super().update(**kwargs)
