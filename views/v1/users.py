from flask import request

from decorators.authenication import authenticate_user
from decorators.request_validations import find_request_by_user

from controllers.users import (
    user_login, user_signup,
    user_fetch, user_update,
    user_delete
)

@find_request_by_user
def login(request_by_user: dict) -> tuple:
    return user_login(body=request_by_user)

@find_request_by_user
def signup(request_by_user: dict) -> tuple:
    return user_signup(body=request_by_user)

def get_user(user_id: str) -> tuple:
    return user_fetch(user_id=user_id)

def update_user(user_id: str, request_by_user: dict={}) -> tuple:
    return user_update(
        user_id=user_id,
        body=request_by_user
    )

def delete_user(user_id: str) -> tuple:
    return user_delete(user_id=user_id)

@authenticate_user
@find_request_by_user
def self_operations(claims: dict, request_by_user: dict) -> tuple:
    if request.method == 'GET':
        return get_user(
                    user_id=claims.get('sub'),
                )

    if request.method == 'PUT':
        return update_user(
                    user_id=claims.get('sub'),
                    request_by_user=request_by_user,
                )

    if request.method == 'DELETE':
        return delete_user(
                    user_id=claims.get('sub'),
                )
