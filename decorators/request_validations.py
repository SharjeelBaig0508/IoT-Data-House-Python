from flask import request
from functools import wraps

def find_request_by_user(function) -> tuple:
    @wraps(function)
    def wrapper(*args, **kwargs) -> tuple:
        request_by_user = {}
        if request.method == 'GET':
            request_by_user = request.args.to_dict()

        if request.method == 'POST':
            if request.is_json:
                request_by_user = request.get_json()
            else:
                return {'message': 'Request for POST method must be a JSON Object'}, 400

        if request.method == 'PUT':
            if request.is_json:
                request_by_user = request.get_json()
            else:
                return {'message': 'Request for PUT method must be a JSON Object'}, 400

        if request.method == 'DELETE':
            request_by_user = request.args.to_dict()

        return function(request_by_user=request_by_user, *args, **kwargs)

    return wrapper
