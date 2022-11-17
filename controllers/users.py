from models.users import User, Status
from schemas.users import user_login_validator, user_signup_validator, user_update_validator
from utils.users import generate_jwt, get_single_user, get_active_user, get_active_users, user_filter

def user_login(body: dict) -> tuple:
    err, verified_data = user_login_validator(body)
    if err:
        return err, 400
    
    db_user: User = get_active_user({'email': verified_data['email']})
    if not db_user:
        return {'message': 'User not found'}, 404
    
    if not db_user.check_password(verified_data['password']):
        return {'message': 'Invalid Password'}, 401
    
    err, token = generate_jwt(user_id=str(db_user.id))
    if err:
        return err, 500

    return token, 200

def user_signup(body: dict) -> tuple:
    err, verified_data = user_signup_validator(body)
    if err:
        return err, 400
    
    if get_active_user({'email': verified_data['email']}):
        return {'message': 'User Email already exists'}, 409
    
    user_model = User(**verified_data)
    user_model.encrypt_password()
    user_model.save()
    
    return {'message': 'User created successfully'}, 201

def user_fetch(user_id: str) -> tuple:
    db_user: User = get_active_user({'id': user_id})
    if not db_user:
        return {'message': 'User not found'}, 404
    
    return {'user': user_filter(db_user)}, 200

def user_update(user_id: str, body: dict) -> tuple:
    db_user: User = get_active_user({'id': user_id})
    if not db_user:
        return {'message': 'User not found'}, 404
        
    err, verified_data = user_update_validator(body)
    if err:
        return err, 400
        
    if verified_data.get('old_password'):
        if not db_user.check_password(verified_data['old_password']):
            return {'message': 'Invalid Password'}, 401
        
        db_user.password = verified_data['new_password']
        db_user.encrypt_password()
        
        verified_data['password'] = db_user.password
        
        del verified_data['old_password']
        del verified_data['new_password']
        del verified_data['confirm_password']
    
    if verified_data:
        db_user.update(**verified_data)
        db_user.reload()
    
    message = 'User updated successfully'
    if verified_data.get('password'):
        message = 'Password changed successfully'
        
    return {
        'message': message,
        'user': user_filter(db_user),
    }, 200

def user_delete(user_id: str) -> tuple:
    db_user: User = get_single_user({'id': user_id})
    if not db_user:
        return {'message': 'User not found'}, 404
    
    db_user.update(status=Status.INACTIVE)
    db_user.reload()
    
    return {'message': 'User has been deleted'}, 200
