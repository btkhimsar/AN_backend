from .models import Category

def request_json(request, user_language):
    # print(request.name[user_language])
    request_data = {'name': request.name[user_language], 'description': request.description[user_language],
                    'default_view_count': request.default_view_count}
    request_data['categories'] = []
    if len(request.categories)!=0:
        for i in request.categories:
            obj = Category.objects(id=i)
            # print(o)
            request_data['categories'].append({'name': obj[0].name[user_language], 'description': obj[0].description[user_language],
                                        'icon_url': obj[0].icon_url, 'has_questions': obj[0].has_questions})
    return request_data
