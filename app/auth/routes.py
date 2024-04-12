import re
from flask import jsonify, request, session, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt, decode_token)
from app.models import User, TokenBlocklist, Profile, Family
from app.auth import bp


def valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def valid_password(password, confirm_password=None):
    if password != confirm_password and confirm_password is not None:
        return False
    if len(password) < 8:
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    return True


def user_exists(email):
    user = User.get_user_by_email(email=email)
    if user is not None:
        return user
    return False


@bp.post('/register')
def register_user():
    data = request.get_json()

    # if not valid_email(email=data.get('email')):
    #     return jsonify(message='not valid email'), False
    #
    # if not valid_password(password=data.get('password'), confirm_password=data.get('confirm_password')):
    #     return jsonify(message='not valid email or password and confirm_password not same'), False
    #
    if user_exists(email=data.get('email')):
        return jsonify({'error': 'User already exists'}), False

    new_family = Family(
        name=data.get('family_name')
    )
    new_family.save()

    new_user = User(
        family_id=new_family.id,
        email=data.get('email')
    )
    new_user.set_password(password=data.get('password'))
    new_user.save()

    user_profile = Profile(
        user_id=new_user.id,
        firstname=data.get('firstname'),
        lastname=data.get('lastname')
    )
    user_profile.save()

    return jsonify({'message': 'User created'}), 200


@bp.post('/login')
def login_user():
    data = request.get_json()
    user = user_exists(data.get('email'))
    # if not valid_password(password=data.get('password')):
    #     return jsonify(message='valid password')

    if user and (user.check_password(password=data.get('password'))):

        access_token = create_access_token(identity=user.id, additional_claims={"family_id": user.family_id})
        refresh_token = create_refresh_token(identity=user.id, additional_claims={"family_id": user.family_id})

        rs = make_response(jsonify(access_token=access_token))
        rs.set_cookie(key='refresh_token_cookie', value=refresh_token, path='/api/auth/refresh', httponly=True, secure=True)
        rs.set_cookie(key='access_token_cookie', value=refresh_token, path='/', httponly=True, secure=True)
        freshen_session(decode_token(encoded_token=access_token))

        return rs, 200

    return jsonify({'error': 'Invalid email or password'})


@bp.get('/whoami')
@jwt_required()
def whoami():
    claims = get_jwt()
    return jsonify({'message': 'message', 'user_deta': claims})


@bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    payload = get_jwt()
    claims = {
        'role': payload.get('role')
    }
    new_access_token = create_access_token(identity=payload.get('sub'), additional_claims=claims)

    return jsonify({'access_token': new_access_token})


def freshen_session(payload):
    session['Id'] = payload['sub']
    session['FamilyId'] = payload['family_id']
    session['AccessIssueTime'] = payload['exp']


@bp.get('/logout')
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    token_b = TokenBlocklist(jti=jti)
    token_b.save()
    return jsonify({'message': f"{token_type} token revoked successfully"}), 200
