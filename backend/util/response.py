import json
import jwt
from http import HTTPStatus
from django.conf import settings
from django.http.response import JsonResponse
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(request):
        auth_token = None
        body_data = json.loads(request.body)
        if 'auth_token' in body_data:
            auth_token = body_data['auth_token']
        if not auth_token:
            return JsonResponse(data=create_resp_dict(False, "Token is missing"), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        try:
            data = jwt.decode(auth_token, key=settings.SECRET_KEY, leeway=20, algorithms=['HS256'])
            if body_data['user_id'] == data['id']:
                return f(request)
        except Exception as e:
            return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)
    return decorated


def create_resp_dict(status, message):
    resp = {
        'isSuccess': False,
        'message': ''
    }
    if status:
        resp['isSuccess'] = True
    resp['message'] = str(message)
    return resp
