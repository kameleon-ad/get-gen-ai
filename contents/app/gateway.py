import requests
from flask import request, current_app

from app.utils import logged_error
from app.api.helper import send_error


def authorization_require():
    """
    Validate token by auth_service
    Args:

    Returns:

    """
    def wrapper(func):
        def decorator(*args, **kwargs):
            auth_endpoint = current_app.config['AUTH_ENDPOINT']
            authorization = request.headers.get('Authorization', '').strip()
            try:
                res = requests.get(auth_endpoint, headers={"Authorization": authorization}).json()
            except Exception as ex:
                logged_error(f"Call validate token api failed: {ex}")
                return send_error(message="You don't have permission")
            if 'message' in res and res['message']['status'] == 'success':
                payload = res['data']
                return func(*args, payload=payload, **kwargs)
            else:
                return send_error(message="You don't have permission")
        return decorator
    return wrapper
