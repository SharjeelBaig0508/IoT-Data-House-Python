from datetime import datetime

from mongoengine import (
    Document, StringField,
    FloatField, DateTimeField,
    ReferenceField,
)


class Stream(Document):
    sensor = ReferenceField('Sensor')
    data = FloatField(
        required=True,
    )
    unit_of_measure = StringField(
        required=True
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
