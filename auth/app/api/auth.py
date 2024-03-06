import json
import uuid
from datetime import timedelta

from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.api.helper import send_error, send_result
from app.utils import logged_input, get_timestamp_now
from app.validator import SignupBodyValidation, LoginBodyValidation, UserSchema
from app.models import User, Token
from app.extensions import SQL_DB

ACCESS_EXPIRES = timedelta(days=1)
REFRESH_EXPIRES = timedelta(days=5)
api_auth_bp = Blueprint('auth', __name__)


@api_auth_bp.get('/status')
def status():
    return jsonify({
        "status": True,
    })


@api_auth_bp.post('/signup')
def signup():
    """
    Signup API.
    Requests Body:
            email: string, require
            password: string, require
    Returns:
            {
                "user_id": id of user
            }
    """

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message='Request Body incorrect json format: ' + str(ex), code=442)

    # Log request api
    logged_input(json.dumps(json_req))
    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    # validate request body
    is_not_validate = SignupBodyValidation().validate(json_body)  # Dictionary show detail error fields
    if is_not_validate:
        return send_error(data=is_not_validate, message='Invalid parameters')

    email = json_body.get('email')
    password = json_body.get('password')
    duplicated_user = User.query.filter(User.email == email).first()
    if duplicated_user:
        return send_error(message='User existed')

    created_date = get_timestamp_now()
    _id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)
    new_user = User(id=_id, email=email, password_hash=password_hash, created_date=created_date)
    SQL_DB.session.add(new_user)
    SQL_DB.session.commit()

    data = {
        'user_id': _id
    }

    return send_result(data=data)


@api_auth_bp.post('/login')
def login():
    """
    Login API

    Requests Body:
            email: string, require
            password: string, require

    Returns:
            {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username,
                ...other info
            }
    """

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message='Request Body incorrect json format: ' + str(ex), code=442)

    logged_input(json.dumps(json_req))
    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        json_body.setdefault(key, str(value).strip())

    # validate request body
    is_not_validate = LoginBodyValidation().validate(json_body)  # Dictionary show detail error fields
    if is_not_validate:
        return send_error(data=is_not_validate, message='Invalid params')

    # Check username and password
    email = json_body.get('email')
    password = json_body.get('password')

    user = User.query.filter(User.email == email).first()
    if user is None or (password and not check_password_hash(user.password_hash, password)):
        return send_error(message='Login failed')

    access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES)
    refresh_token = create_refresh_token(identity=user.id, expires_delta=REFRESH_EXPIRES)

    # Store the tokens in our store with a status of not currently revoked.
    Token.add_token_to_database(access_token, user.id)
    Token.add_token_to_database(refresh_token, user.id)

    data: dict = UserSchema().dump(user)
    data.setdefault('access_token', access_token)
    data.setdefault('refresh_token', refresh_token)

    return send_result(data=data, message='Logged in successfully!')


@api_auth_bp.get('/tokens/validate')
def validate_token():
    """
    Validate access_token api

    Requests Header:
            Authorization: string, require

    Returns:
            validate or not
    """
    _, payload = verify_jwt_in_request()
    return send_result(message=f'Token valid', data=payload)
