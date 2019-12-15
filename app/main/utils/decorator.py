from functools import wraps

from flask import request
from app.main.services.auth_helper import Auth


def add_access_token_header(api):
    parser = api.parser()
    parser.add_argument('Authorization', type=str,
                        location='headers',
                        help='Bearer Access Token',
                        required=True)

    return api.doc(parser=parser)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')
        if not token:
            return data, status
        kwargs['user_id'] = token.get('user_id')
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
