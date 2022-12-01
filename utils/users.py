import os
import jwt

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

        return {}, jwt.encode(
                        claims,
                        os.environ.get('SECRET_KEY', 'anything_goes_with_123@'),
                        algorithm='HS256'
                    ).decode()
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

def user_filter(user: Document, fields_to_keep: list) -> dict:
    user: dict = user.to_mongo().to_dict()

    applyFormat = {
        'createdAt': datetime.isoformat,
        'updatedAt': datetime.isoformat,
    }

    for field in applyFormat:
        user[field] = applyFormat[field](user[field])

    return {field: user.get(field) for field in fields_to_keep}

def multi_user_filter(users: QuerySet, fields_to_keep: list) -> list:
    return [
        user_filter(
            user=user,
            fields_to_keep=fields_to_keep,
        )
        for user in users
    ]
