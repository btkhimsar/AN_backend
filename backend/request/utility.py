from Constants.image_urls import HOME_ICON


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json(request):
    request_data = {'type': 'request', 'mobile': request.mobile, 'subtitle_icon': HOME_ICON,
                    'title': request.title}
    return request_data
