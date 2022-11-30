import os
import jwt
import json

from models.users import User, Status
from datetime import datetime, timedelta
from mongoengine import Document, QuerySet
from utils.common import get_single_record, get_records


def generate_jwt(user_id: str) -> tuple:
    try:
        claims = {
            'sub': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=int(os.environ.get('LOGIN_EXP', '1')))
        }

        return {}, {'token':
                        jwt.encode(
                            claims,
                            os.environ.get('SECRET_KEY', 'anything_goes_with_123@'),
                            algorithm='HS256'
                        ).decode()
                    }
    except Exception:
        return {'message': 'Error Occured while generating Authorization Token'}, {}

def get_single_user(user_filter: dict) -> Document:
    return get_single_record(User, user_filter)

def get_users(user_filter: dict) -> QuerySet:
    return get_records(User, user_filter)

def get_active_user(user_filter: dict) -> Document:
    user_filter['status'] = Status.ACTIVE
    return get_single_record(User, user_filter)

def get_active_users(user_filter: dict) -> QuerySet:
    user_filter['status'] = Status.ACTIVE
    return get_records(User, user_filter)

user_fields_to_keep = ['name', 'email', 'status']

def user_filter(user: Document) -> dict:
    user = json.loads(user.to_json())
    return {k: user[k] for k in user_fields_to_keep}

def multi_user_filter(users: QuerySet) -> list:
    user_list = []
    for user in users:
        user_list.append(user_filter(user))

    return user_list
