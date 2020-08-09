from Constants.image_urls import HOME_ICON


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json_for_myrequests(request):
    request_data = {'type': 'request', 'mobile': request.mobile, 'subtitle_icon': HOME_ICON,
                    'category_id': request.category_id, 'radius': request.radius, 'location': request.location,
                    'comment': request.comment, 'created_at': request.created_at, 'user_id': request.user_id,
                    'isCompleted': request.isCompleted, 'isPaid': request.isPaid, 'isExpired':request.isExpired,
                    'provider_id': request.provider_id, 'complaints': request.complaints, 'requestId': str(request.id),
                    'title': 'You requested for'}
    return request_data

def request_json_for_workrequests(request):
    request_data = {'type': 'request', 'mobile': request.mobile, 'subtitle_icon': HOME_ICON,
                    'category_id': request.category_id, 'radius': request.radius, 'location': request.location,
                    'created_at': request.created_at, 'user_id': request.user_id,
                    'provider_id': request.provider_id, 'complaints': request.complaints, 'requestId': str(request.id)}
    return request_data
