import datetime
import jwt
from django.conf import settings
from category.models import Category


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
                                            minutes=30)}, key=settings.SECRET_KEY, algorithm='HS256')
    return request_auth_token


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point
