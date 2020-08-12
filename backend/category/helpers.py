from .models import Category

def request_json(request, user_language):
    request_data = {'name': request.name[user_language], 'description': request.description[user_language],
                    'default_view_count': request.default_view_count}
    request_data['categories'] = []
    if len(request.categories)!=0:
        for i in request.categories:
            obj = Category.objects.get(id=i)
            request_data['categories'].append({'name': obj.name[user_language], 'description': obj.description[user_language],
                                        'icon_url': obj.icon_url, 'has_questions': obj.has_questions})
    return request_data
