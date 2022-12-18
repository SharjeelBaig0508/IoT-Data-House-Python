from flask import Blueprint
from views.v1 import users

# All the methods used in backend APIs
GET, POST, PUT, DELETE = 'GET', 'POST', 'PUT', 'DELETE'

v1_views = Blueprint('v1_views', __name__, url_prefix='/api/v1')

# All routes available
all_rules = {
    'user': [
        # ROUTE, VIEW, METHODS
        [
            '/user/login',
            users.login,
            [POST],
        ],
        [
            '/user/signup',
            users.signup,
            [POST],
        ],
        [
            '/user',
            users.self_operations,
            [GET, PUT, DELETE],
        ],
    ],
}

for type in all_rules:
    for rule in all_rules[type]:
        v1_views.add_url_rule(rule[0], view_func=rule[1], methods=rule[2])
