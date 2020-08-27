import json
from http import HTTPStatus
import requests
import jwt
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings

from Constants.response_strings import *
from Constants.otp import *
from setup import client
from util.response import create_resp_dict
from .models import User
from .utility import create_user_dict, create_point_dict
from category.models import Category
from .constants import body, headers


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
                if len(user_query) == 0:
                    # todo generate a random otp and message the user
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True
                elif len(user_query[0].name)==0:
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True
                else:
                    user = User.objects.get(mobile=mobile)
                    resp = create_resp_dict(True, USER_EXISTS)
                    resp['user'] = {"name": user.name, "user_language": user.user_language}
                    resp['newuser'] = False
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
                user = User.objects.get(id=user_id)
                user_type = user.user_type
                resp = create_resp_dict(True, USER_UPDATED)
                for key in user_data:
                    if user_type=='provider':
                        if key!='mobile' and key!='user_type':
                            if key=='base_location':
                                location = create_point_dict(user_data[str(key)]['latitude'], user_data[str(key)]['longitude'])
                                user[str(key)] = location
                            elif key=='work_category' and user[str(key)] is not None:
                                resp['user_details'] = "User's work_category, name can't be changed."
                            else:
                                if key=='work_category':
                                    category = Category.objects.get(id=user_data[key])
                                user[str(key)] = user_data[str(key)]
                        else:
                            resp['user_details'] = "User's mobile, user_type, name can't be changed."
                    else:
                        if key!='mobile' and key!='user_type':
                            user[str(key)] = user_data[str(key)]
                        else:
                            resp['user_details'] = "User's mobile, user_type, name can't be changed."
                user.save()
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
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
                user_otp = body_data['user_otp']
                name = body_data['name']
                user_language = body_data['user_language']
                token = body_data['token']
                if user_otp == otp:
                    user_count = User.objects(mobile=mobile)
                    if len(user_count)==0:
                        user_type = body_data['user_type']
                        user = User(mobile=mobile, name=name, user_type=user_type, user_language=user_language, token=token)
                        user.save()
                        auth_token = jwt.encode(payload={'id': str(user.id), 'num': str(user.mobile)},
                                                key=settings.SECRET_KEY,
                                                algorithm='HS256')
                        # print(jwt.decode(auth_token), 'settings.SECRET_KEY', algorithms=['HS256'])
                        resp_data = create_resp_dict(True, AUTH_SUCCESS)
                        resp_data['auth_token'] = auth_token.decode('utf-8')
                        resp_data['user_id'] = str(user.id)
                    else:
                        auth_token = jwt.encode(payload={'id': str(user_count[0].id), 'num': str(user_count[0].mobile)},
                                                key=settings.SECRET_KEY,
                                                algorithm='HS256')
                        decoded = jwt.decode(auth_token, 'settings.SECRET_KEY', algorithms='HS256', verify=False)
                        print(decoded)
                        print(jwt.get_unverified_header(auth_token))
                        resp_data = create_resp_dict(True, AUTH_SUCCESS)
                        resp_data['auth_token'] = auth_token.decode('utf-8')
                        resp_data['user_id'] = str(user_count[0].id)
                        resp_data['user_details'] = create_user_dict(user_count[0])
                        if user_count[0].work_category is not None:
                            resp_data['user_details']['work_category_id'] = str(user_count[0].work_category)
                        resp_data['user_exists'] = "User's name, user_type can't be changed."
                    return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
                else:
                    return JsonResponse(data=create_resp_dict(False, AUTH_FAIL), safe=False,
                                        status=HTTPStatus.UNAUTHORIZED)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)

