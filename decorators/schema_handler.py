from functools import wraps
from marshmallow import ValidationError

def validation_error_handler(function) -> tuple:
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ValidationError as err:
            return {
                    'errors': err.messages,
                    'message': 'Some fields are invalid'
                    }, {}

    return wrapper
