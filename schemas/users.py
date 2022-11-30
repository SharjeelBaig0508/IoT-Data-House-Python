# -------------< Imports >-------------
from marshmallow import (
    Schema,
    fields,
    ValidationError,
    validates_schema,
)
from decorators.schema_handler import validation_error_handler

# -------------< Schemas >-------------
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserSignUpSchema(Schema):
    name = fields.String()
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserUpdateSchema(Schema):
    name = fields.String()
    old_password = fields.String()
    new_password = fields.String()
    confirm_password = fields.String()

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data.get('old_password'):
            if not (data.get('new_password') and data.get('confirm_password')):
                raise ValidationError('if one is provided all will be provided', 'old_password')

        if data.get('new_password'):
            if not (data.get('old_password') and data.get('confirm_password')):
                raise ValidationError('if one is provided all will be provided', 'new_password')

        if data.get('confirm_password'):
            if not (data.get('old_password') and data.get('new_password')):
                raise ValidationError('if one is provided all will be provided', 'confirm_password')

        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError('new_password and confirm_password must be same', 'confirm_password')

        if data.get('old_password') and data.get('new_password'):
            if data['old_password'] == data['new_password']:
                raise ValidationError('new_password must not be same as old_password', 'new_password')

# -------------< Validators >-------------
@validation_error_handler
def user_login_validator(body):
    return {}, UserLoginSchema().load(body)

@validation_error_handler
def user_signup_validator(body):
    return {}, UserSignUpSchema().load(body)

@validation_error_handler
def user_update_validator(body):
    return {}, UserUpdateSchema().load(body)
