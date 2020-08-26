from .models import Category, Question

def request_json(request, user_language):
    request_data = {'name': request.name[user_language], 'description': request.description[user_language],
                    'default_view_count': request.default_view_count, 'super_category_id': str(request.id)}
    request_data['categories'] = []
    if len(request.categories)!=0:
        for i in request.categories:
            obj = Category.objects.get(id=i)
            request_data['categories'].append({'name': obj.name[user_language], 'description': obj.description[user_language],
                                        'icon_url': obj.icon_url, 'has_questions': obj.has_questions, 'category_id': i})
    return request_data

def request_json_for_question(question_id, user_language):
    question = Question.objects.get(id=question_id)
    request_data = {}
    request_data['question_id'] = str(question.id)
    request_data['type'] = question.type
    request_data['text'] = question.text[user_language]
    request_data['isMandatory'] = question.isMandatory
    request_data['answers'] = []
    for i in question.answers:
        data = {}
        data['answer_id'] = i.answer_id
        data['text'] = i.text[user_language]
        request_data['answers'].append(data)
    return request_data