import datetime
import jwt
from django.conf import settings
import pyotp
import requests
from .models import ProviderInfo
from category.models import Category
from .constants import params


def request_json_for_provider(provider_info, language, resp):
    if provider_info.loc_name:
        resp['user']['loc_name'] = provider_info.loc_name
    if provider_info.category:
        category_list = Category.objects(id__in=provider_info.category)
        resp['user']['category'] = []
        for each_category in category_list:
            resp['user']['category'].append(each_category.name[language])
    if provider_info.radius:
        resp['user']['radius'] = provider_info.radius
    if provider_info.is_active:
        resp['user']['is_active'] = provider_info.is_active


def create_user_dict(user, resp):
    resp['user'] = {'user_id': str(user.id), 'mobile': user.mobile, 'name': user.name, 'language': user.language,
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


def verify_otp(otp):
    current_time = datetime.datetime.now()
    totp = pyotp.TOTP('base32secret3232')
    for i in range(-60, 1):
        if str(otp) == str(totp.at(current_time, i)):
            return True
    return False


def generate_otp(mobile):
    totp = pyotp.TOTP('base32secret3232')
    return totp.now()
    # send_sms(mobile, totp.now())


def send_sms(mobile, generated_otp):
    params['receiver'] = mobile
    params['sms'] = 'Your otp is {}'.format(generated_otp)
    requests.get('http://staticking.org/index.php/smsapi/httpapi/', params=params)


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
            category_list = Category.objects(id__in=user_data[key])
            for category in user_data[key]:
                if info.category.count(category) == 0:
                    info.category.append(category)
        elif key == 'radius':
            info.radius = user_data[key]
        elif key == 'rating':
            user.rating = user_data[key]
    user.provider_info = info
    user.save()
