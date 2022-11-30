import os
import jwt

from functools import wraps
from flask import request, g

def authenticate_user(function) -> tuple:
    @wraps(function)
    def verify_token(*args, **kwargs) -> tuple:
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Authorization Token must be provided'}, 401

        if type(token) is not str:
            return {'message': 'Authorization Token must be a string'}, 401

        splitted_token = token.split(' ')
        if splitted_token[0] != 'Bearer':
            return {'message': 'Authorization Token must be a Bearer Token'}, 401

        token = splitted_token[-1]

        try:
            g.claims = jwt.decode(token, os.environ.get('SECRET_KEY', 'anything_goes_with_123@'))

        except jwt.ExpiredSignatureError:
            return {'message': 'Authorization Token is Expired'}, 498

        except jwt.InvalidTokenError:
            return {'message': 'Authorization Token is Invalid'}, 498

        return function(
            claims=g.claims,
            *args,
            **kwargs,
        )

    return verify_token
