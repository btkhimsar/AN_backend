import json
from http import HTTPStatus

import jwt
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings

from Constants.response_strings import *
from setup import client
from util.response import create_resp_dict
from .models import User
from .utility import create_user_dict


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                mobile = body_data['mobile']
                user_query = User.objects(mobile=mobile)
                print(mobile)
                print(len(user_query))
                if len(user_query) == 0:
                    # todo generate a random otp and message the user
                    user = User(mobile=mobile)
                    user.save()
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True
                    return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
                elif len(user_query[0].name)==0 or len(user_query[0].user_type)==0 or len(user_query[0].user_language)==0:
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True
                    return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
                else:
                    resp = create_resp_dict(True, USER_EXISTS)
                    resp['newuser'] = False
                    resp['user'] = create_user_dict(user_query[0])
                    return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def update_profile(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                # todo verify auth token
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                user_data = body_data['user']
                user = User.objects(id=user_id).first()
                print(user.mobile)
                for key in user_data:
                    user[str(key)] = user_data[str(key)]
                user.save()
                return JsonResponse(data=create_resp_dict(True, USER_UPDATED), safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)

@api_view(['POST'])
def profile(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                # todo verify auth token
                auth_token = body_data['auth_token']

                user_id = body_data['user_id']
                user = User.objects(id=user_id).first()
                user_details = create_user_dict(user)
                resp = create_resp_dict(True, USER_FETCHED)
                resp['user'] = user_details
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def auth(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                mobile = body_data['mobile']
                otp = body_data['otp']
                name = body_data['name']
                user_type = body_data['user_type']
                user_language = body_data['user_language']
                user = User.objects(mobile=mobile)[0]
                print(mobile)
                if user.otp == otp:
                    # user = json.loads(user)
                    auth_token = jwt.encode(payload={'id': str(user.id), 'num': str(user.mobile)},
                                            key=settings.SECRET_KEY,
                                            algorithm='HS256')
                    # user = User(mobile=mobile, name=name, user_type=user_type, language=language)
                    # user.save()
                    user.name = name
                    user.user_type = user_type.lower()
                    user.user_language = user_language.lower()
                    user.save()
                    resp_data = create_resp_dict(True, AUTH_SUCCESS)
                    resp_data['auth_token'] = auth_token.decode('utf-8')
                    resp_data['user_id'] = str(user.id)
                    return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
                else:
                    return JsonResponse(data=create_resp_dict(False, AUTH_FAIL), safe=False,
                                        status=HTTPStatus.UNAUTHORIZED)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
