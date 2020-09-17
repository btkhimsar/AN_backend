import datetime
import jwt
from util.response import create_resp_dict
from django.conf import settings
from category.models import Category
import pyotp
from http import HTTPStatus
from twilio.rest import Client
from django.http.response import JsonResponse


def create_user_dict(user):
    user_details = {'mobile': user.mobile, 'name': user.name, 'user_language': user.user_language,
                    'user_type': user.user_type, 'token': user.token, 'active': user.active}
    if user.work_category:
        category = Category.objects.get(id=user.work_category)
        user_details['work_category'] = category.name[user.user_language]
    if user.base_location:
        user_details['base_location'] = user.base_location
    if user.work_radius:
        user_details['work_radius'] = user.work_radius
    if user.email:
        user_details['email'] = user.email
    if user.address:
        user_details['address'] = user.address
    return user_details


def generate_auth_token(user):
    request_auth_token = jwt.encode(payload={'id': str(user.id), 'num': str(user.mobile),
                                             'exp': datetime.datetime.utcnow() + datetime.timedelta(
                                                 hours=6)}, key=settings.SECRET_KEY, algorithm='HS256')
    return request_auth_token


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def generate_otp(mobile):
    totp = pyotp.TOTP('base32secret3232')
    generated_otp = totp.now()
    check = send_sms(mobile, generated_otp)
    if check is None:
        return "OTP generated"
    else:
        return "Unverified Number"


def send_sms(mobile, generated_otp):
    try:
        account_sid = 'AC3b002160acdc829f1f84d9d791e1ae71'
        auth_token = 'c62aca92bc25d65e54a9b33a39c397f3'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='Your OTP is' + str(generated_otp), from_='+12095632935',
            to='+91'+str(mobile))
        # print(message.sid)
    except Exception as e:
        return "Unverified Number"


