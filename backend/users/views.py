import json
from http import HTTPStatus
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from Constants.response_strings import *
from util.response import create_resp_dict, token_required
from .models import User
from .utility import *
import request


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

                user = User.objects(mobile=mobile)

                if len(user) == 0:
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True
                    resp['otp'] = generate_otp(mobile)

                elif len(user[0].name) == 0:
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True
                    resp['otp'] = generate_otp(mobile)

                else:
                    resp = create_resp_dict(True, USER_EXISTS)
                    resp['name'] = user[0].name
                    resp['newuser'] = False
                    resp['otp'] = generate_otp(mobile)

                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
@token_required
def update_profile(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))

                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                user_data = body_data['user']

                user = User.objects.get(id=user_id)

                resp = create_resp_dict(True, USER_UPDATED)

                for key in user_data:
                    if key == 'email':
                        user[key] = user_data[key]
                    elif key == 'pic_url':
                        user[key] = user_data[key]
                if user.user_type == 'provider':
                    update_provider_info(user, user_data, resp)

                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
@token_required
def profile(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']

                user = User.objects.get(id=user_id)

                resp = create_resp_dict(True, USER_FETCHED)
                create_user_dict(user, resp)

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
                language = body_data['language']
                fcm_token = body_data['fcm_token']

                user = User.objects(mobile=mobile)

                if verify_otp(otp):
                    if len(user) == 0:
                        user_type = body_data['user_type']
                        new_user = User(mobile=mobile, name=name, user_type=user_type,
                                        language=language, fcm_token=fcm_token)
                        new_user.save()

                        auth_token = generate_auth_token(new_user)
                        resp_data = create_resp_dict(True, AUTH_SUCCESS)

                        resp_data['auth_token'] = auth_token.decode('utf-8')
                        resp_data['user_id'] = str(new_user.id)

                    else:
                        auth_token = generate_auth_token(user[0])
                        resp_data = create_resp_dict(True, AUTH_SUCCESS)

                        resp_data['auth_token'] = auth_token.decode('utf-8')
                        create_user_dict(user[0], resp_data)

                    return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)

                else:
                    return JsonResponse(data=create_resp_dict(False, AUTH_FAIL), safe=False,
                                        status=HTTPStatus.UNAUTHORIZED)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def is_active(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                is_active = body_data['is_active']

                user = User.objects.get(id=user_id)
                if user.user_type == 'provider':
                    user.is_active = is_active
                    user.save()
                    resp = create_resp_dict(True, USER_UPDATED)
                else:
                    resp = create_resp_dict(False, 'User Not Updated')
                    resp['error_code'] = 103

                return JsonResponse(data=resp, safe=False,
                                    status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)

