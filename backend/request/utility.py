from Constants.image_urls import HOME_ICON
from category.models import Category
from users.models import User

def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json_for_myrequests(request):
    request_data = {'type': 'request', 'comment': request.comment,'isCompleted': request.isCompleted,
                    'isPaid': request.isPaid, 'isExpired':request.isExpired, 'provider_id': request.provider_id,
                    'requestId': str(request.id)}
    user = User.objects.get(id=request.user_id)
    category = Category.objects.get(id=request.category_id)
    request_data['subtitle'] = category.name[user.user_language]
    if user.user_language=='english':
        request_data['title'] = "You requested for"
    elif user.user_language=='hindi':
        request_data['title'] ='आपने निवेदन किया'
    return request_data

def request_json_for_workrequests(request):
    request_data = {'type': 'request', 'mobile': request.mobile, 'subtitle_icon': HOME_ICON,
                    'category_id': request.category_id, 'location': request.location,
                    'created_at': request.created_at, 'user_id': request.user_id,
                    'provider_id': request.provider_id, 'complaints': request.complaints, 'requestId': str(request.id)}
    return request_data
