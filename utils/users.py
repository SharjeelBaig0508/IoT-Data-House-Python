from os import environ
from jwt import encode
from json import loads
from datetime import datetime, timedelta

def generate_jwt(user_id):
    try:
        claims = {
            'sub': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=int(environ.get('LOGIN_EXP', '1')))
        }
        
        return {}, {'token': 
                        encode(
                            claims, 
                            environ.get('SECRET_KEY', 'anything_goes_with_123@'), 
                            algorithm='HS256'
                        ).decode()
                    }
    except Exception:
        return {'message': 'Error Occured while generating Authorization Token'}, {}

user_fields_to_keep = ['name', 'email', 'status']

def user_filter(user):
    user = loads(user.to_json())
    return {k: user[k] for k in user_fields_to_keep}
