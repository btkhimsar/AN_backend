import requests
from .constants import body, headers, get_month
from datetime import datetime, date
from users.models import User


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json_for_myrequest(my_request, category, user_language):
    request_data = {'type': 'request', 'title': category.name[user_language], 'isCompleted': my_request.isCompleted,
                    'request_id': my_request._id, 'expiry_text': 'Expires in 7 days'}

    return request_data


def request_json_for_workrequest(work_request, user_language):
    user = User.objects.get(_id=work_request.user_id)
    request_data = {'title': work_request.location_name, 'image_url': user.profile_image, 'mobile': work_request.mobile,
                    'type': 'request', 'name': user.name, 'request_id': work_request._id}
    get_date = convert_timestamps(work_request.created_at)
    request_data['created_date'] = str(get_date.day) + ' ' + str(get_month[get_date.month][user_language])
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


def location_text(language, isCompleted_requests, category):
    if language == 'english':
        return "{} active requests for {} near".format(isCompleted_requests, category.name[language])
    elif language == 'hindi':
        return "निकट {} के लिए {} सक्रिय कार्य अनुरोध".format(category.name[language], isCompleted_requests)


def notification(users_list, location_name):
    for user in users_list:
        body['to'] = user.token
        body['data']['title'] = '{} from {} requested for your service'.format(user.name, location_name)
        requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=body)


def categories_dict(categories_list):
    request_dict = {}
    for category in categories_list:
        request_dict[str(category.id)] = category
    return request_dict


def super_categories_dict(super_categories_list):
    request_dict = {}
    for super_category in super_categories_list:
        request_dict[str(super_category.id)] = super_category
    return request_dict


def today_date():
    today = datetime.now()
    today_timestamp = datetime.timestamp(today)
    return date.fromtimestamp(today_timestamp)


def convert_timestamps(timestmp):
    return date.fromtimestamp(timestmp)


def my_requests_list_func(fetched_requests, categories, user_language):
    ongoing_requests = []
    other_requests = []

    if len(ongoing_requests) == 0:
        header_for_ongoing_requests(ongoing_requests, user_language)

        for request in fetched_requests:

            get_date = convert_timestamps(request.created_at)
            diff = get_date - today_date()

            request_obj = request_json_for_myrequest(request, categories[request.category_id], user_language)
            request_obj['subtitle'] = str(get_date.day) + ' ' + str(get_month[get_date.month][user_language])

            if diff.days <= 7 and (request.isCompleted == False):
                ongoing_requests.append(request_obj)
            else:
                if len(other_requests) == 0:
                    header_for_other_requests(other_requests, user_language)
                other_requests.append(request_obj)

    return ongoing_requests + other_requests


def work_requests_list(fetched_requests, user_language):
    requests_list = []
    for request in fetched_requests:
        request_obj = request_json_for_workrequest(request, user_language)
        requests_list.append(request_obj)
    return requests_list


def get_questions_dict(questions):
    questions_dict = {}
    for question in questions:
        questions_dict[question.id] = question
    return questions_dict


def request_json_for_question(ques_obj, question, user_language):
    request_data = {'title': ques_obj.text[user_language], 'subtitle': ''}
    for ans_id in question.aId:
        ans_obj = ques_obj.answers.filter(answer_id=ans_id)
        request_data['subtitle'] += ans_obj.text[user_language] + " . "
    return request_data


def get_questions(questions, questions_dict, user_language):
    questions_list = []
    for question in questions:
        ques_obj = questions_dict[question['qId']]
        questions_list.append(request_json_for_question(ques_obj, question, user_language))

    return questions_list


def request_json_for_user(user):
    request_data = {'profile_image': user.profile_image, 'name': user.name,
                    'user_id': user._id, 'mobile': user.mobile}
    return request_data


def get_user_details(users_list):
    users_details_list = []
    for user in users_list:
        user_obj = request_json_for_user(user)
        users_details_list.append(user_obj)
    return users_details_list
