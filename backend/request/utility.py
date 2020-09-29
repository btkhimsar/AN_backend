import requests
from .constants import body, headers, get_month, get_hour_string
from datetime import datetime, date
from users.models import User


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json_for_myrequest(my_request, category, language):
    request_data = {'type': 'request', 'title': category.name[language], 'is_completed': my_request.is_completed,
                    'request_id': str(my_request.id), 'expiry_text': 'Expires in 7 days'}
    if my_request.new_interest_count:
        request_data['new_interest_count'] = my_request.new_interest_count
    return request_data


def get_datetime(id, language):
    created_at = id.generation_time
    if created_at.day == datetime.now().day:
        return "{} {}".format(created_at.hour, get_hour_string[language])
    else:
        return str(created_at.day) + ' ' + str(get_month[created_at.month][language])


def request_json_for_workrequest(work_request, language, questions_dict):
    user = User.objects.get(id=work_request.user_id)

    request_data = {'req_id': str(work_request.id), 'reqby_name': user.name, 'reqby_rating': user.rating,
                    'loc_name': work_request.location,
                    'work': get_questions(work_request.questions, questions_dict, language)}
    if user.pic_url:
        request_data['reqby_img'] = user.pic_url
    if work_request.aud_url:
        request_data['aud_url'] = work_request.aud_url
    if work_request.share_mobile == True:
        request_data['mobile'] = user.mobile
    request_data['created_at'] = get_datetime(work_request.id, language)

    return request_data


def header_for_ongoing_requests(requests_list, language):
    if language == 'english':
        requests_list.append({'title': 'Ongoing Requests', 'type': 'header'})
    elif language == 'hindi':
        requests_list.append({'title': 'चल रहे अनुरोध', 'type': 'header'})


def header_for_other_requests(requests_list, language):
    if language == 'english':
        requests_list.append({'title': 'Other Requests', 'type': 'header'})
    elif language == 'hindi':
        requests_list.append({'title': 'अन्य अनुरोध', 'type': 'header'})


def location_text(language, is_completed_requests):
    if language == 'english':
        loc_text = "{} active requests".format(is_completed_requests)
    elif language == 'hindi':
        loc_text = "{} सक्रिय कार्य अनुरोध".format(is_completed_requests)


def notification(users_list, location_name):
    for user in users_list:
        body['to'] = user.fcm_token
        body['data']['title'] = '{} from {} requested for your service'.format(user.name, location_name)
        requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=body)


def categories_dict(categories_list):
    request_dict = {}
    for category in categories_list:
        request_dict[str(category.id)] = category
    return request_dict


def my_requests_list_func(fetched_requests, categories, language):
    ongoing_requests = []
    other_requests = []

    if len(fetched_requests):
        header_for_ongoing_requests(ongoing_requests, language)

        for request in fetched_requests:

            get_date = request.id.generation_time
            diff = get_date.day - datetime.now().day

            request_obj = request_json_for_myrequest(request, categories[request.category_id], language)
            request_obj['subtitle'] = str(get_date.day) + ' ' + str(get_month[get_date.month][language])

            if diff <= 7 and (request.is_completed == False):
                ongoing_requests.append(request_obj)
            else:
                if len(other_requests) == 0:
                    header_for_other_requests(other_requests, language)
                other_requests.append(request_obj)

    return ongoing_requests + other_requests


def work_requests_list(fetched_requests, language, questions_dict):
    requests_list = []
    for request in fetched_requests:
        request_obj = request_json_for_workrequest(request, language, questions_dict)
        requests_list.append(request_obj)
    return requests_list


def get_questions_dict(questions):
    questions_dict = {}
    for question in questions:
        questions_dict[str(question.id)] = question
    return questions_dict


def request_json_for_question(ques_obj, language, answer):
    request_data = {'title': ques_obj.text[language]}

    if ques_obj.question_type == 'text':
        request_data['subtitle'] = answer

    elif ques_obj.question_type == 'select-one':
        ans_obj = ques_obj.answers.filter(ans_id=answer)[0]
        request_data['subtitle'] = ans_obj.text[language]

    elif ques_obj.question_type == 'select-many':
        ans_string = ""
        for ans_id in answer:
            ans_obj = ques_obj.answers.filter(ans_id=ans_id)[0]
            ans_string += ans_obj.text[language] + " . "
        request_data['subtitle'] = ans_string[:-3]

    return request_data


def get_questions(questions, questions_dict, language):
    questions_list = []
    for qId in questions:
        ques_obj = questions_dict[qId]
        questions_list.append(request_json_for_question(ques_obj, language, questions[qId]))

    return questions_list


def request_json_for_user(user):
    request_data = {'name': user.name, 'user_id': user.id, 'mobile': user.mobile}
    if user.pic_url:
        request_data['pic_url'] = user.pic_url
    return request_data


def get_provider_details(users_list):
    providers_list = []
    for user in users_list:
        user_obj = request_json_for_user(user)
        providers_list.append(user_obj)
    return providers_list


def notification_to_consumer(consumer, provider):
    body['to'] = consumer.fcm_token
    body['data']['title'] = '{} has requested for your service.'.format(provider.name)
    requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=body)
