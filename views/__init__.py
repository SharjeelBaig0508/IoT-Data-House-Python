from flask import Blueprint
from views.v1.users import (
    login as user_login,
    signup as user_signup,
    self_operations as user_on_self,
)

v1_views = Blueprint('v1_views', __name__, url_prefix='/api/v1')

v1_views.add_url_rule('/user/login', view_func=user_login, methods=['POST'])

v1_views.add_url_rule('/user/signup', view_func=user_signup, methods=['POST'])

v1_views.add_url_rule('/user', view_func=user_on_self, methods=['GET', 'PUT', 'DELETE'])
