from bcrypt import hashpw, gensalt, checkpw

from enum import Enum
from database_layer import db
from mongoengine import EmailField, StringField, EnumField


class Status(Enum):
    ACTIVE = 0
    INACTIVE = 1

class User(db.Document):
    name            = StringField()
    email           = EmailField(required=True)
    password        = StringField(required=True)
    status          = EnumField(Status, default=Status.ACTIVE)
    
    def encrypt_password(self):
        if type(self.password) is not str:
            self.password = str(self.password)
                
        self.password = hashpw(self.password.encode(), gensalt(rounds=7)).decode()

    def check_password(self, password:str):
        return checkpw(password.encode(), self.password.encode())
