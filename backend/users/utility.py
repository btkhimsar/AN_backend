import datetime
import jwt
from django.conf import settings
import pyotp
from twilio.rest import Client
from .models import ProviderInfo
from category.models import Category


def request_json_for_provider(provider_info, language, resp):
    if provider_info.loc_name:
        resp['user']['loc_name'] = provider_info.loc_name
    if provider_info.category:
        category_name = Category.objects.get(_id=provider_info.category).name[language]
        resp['user']['category'] = category_name
    if provider_info.radius:
        resp['user']['radius'] = provider_info.radius


def create_user_dict(user, resp):
    resp['user'] = {'_id': user._id, 'mobile': user.mobile, 'name': user.name, 'language': user.language,
                    'user_type': user.user_type}
    if user.email:
        resp['user']['email'] = user.email
    if user.pic_url:
        resp['user']['pic_url'] = user.pic_url
    if user.user_type == 'provider' and user.provider_info:
        if user.rating:
            resp['user']['rating'] = user.rating
        request_json_for_provider(user.provider_info, user.language, resp)


def generate_auth_token(user):
    request_auth_token = jwt.encode(payload={'id': str(user.id),
                                             'exp': datetime.datetime.utcnow() + datetime.timedelta(
                                            days=1)}, key=settings.SECRET_KEY, algorithm='HS256')
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
            to='+91' + str(mobile))

    except Exception as e:
        return "Unverified Number"


def update_provider_info(user, user_data, resp):
    info = ProviderInfo()
    for key in user_data:
        if key == 'is_active':
            info.is_active = user_data[key]
        elif key == 'loc_name':
            info.loc_name = user_data[key]
        elif key == 'loc':
            point = create_point_dict(user_data[key]['latitude'], user_data[key]['longitude'])
            info.loc = point
        elif key == 'category':
            if info.category is None:
                category = Category.objects.get(_id=user_data[key])
                info.category = user_data[key]
            else:
                resp['error_code'] = 101
        elif key == 'radius':
            info.radius = user_data[key]
        elif key == 'rating':
            user.rating = user_data[key]
    user.provider_info = info
    user.save()