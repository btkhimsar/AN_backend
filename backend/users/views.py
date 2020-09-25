import json
from http import HTTPStatus
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from Constants.response_strings import *
from Constants.otp import user_otp
from util.response import create_resp_dict, token_required
from .models import User
from .utility import *


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

                elif len(user[0].name) == 0:
                    resp = create_resp_dict(True, OTP_GENERATED)
                    resp['newuser'] = True

                else:
                    resp = create_resp_dict(True, USER_EXISTS)
                    resp['name'] = {"name": user[0].name}
                    resp['newuser'] = False
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

                user = User.objects.get(_id=user_id)

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

                user = User.objects.get(_id=user_id)

                resp = create_resp_dict(True, USER_FETCHED)
                resp['user'] = create_user_dict(user)

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

                if otp == user_otp:

                    if len(user) == 0:
                        user_type = body_data['user_type']
                        new_user = User(mobile=mobile, name=name, user_type=user_type,
                                        language=language, fcm_token=fcm_token, _id=User.objects.count()+1)
                        new_user.save()

                        auth_token = generate_auth_token(new_user)
                        resp_data = create_resp_dict(True, AUTH_SUCCESS)

                        resp_data['auth_token'] = auth_token.decode('utf-8')
                        resp_data['user_id'] = new_user._id

                    else:
                        auth_token = generate_auth_token(user[0])
                        resp_data = create_resp_dict(True, AUTH_SUCCESS)

                        resp_data['auth_token'] = auth_token.decode('utf-8')
                        resp_data['user_id'] = user[0]._id
                        resp_data['user'] = create_user_dict(user[0])

                    return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)

                else:
                    return JsonResponse(data=create_resp_dict(False, AUTH_FAIL), safe=False,
                                        status=HTTPStatus.UNAUTHORIZED)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)

