import requests
from .constants import body, headers, get_month
from datetime import datetime, date
from users.models import User


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json_for_myrequest(my_request, category, language):
    request_data = {'type': 'request', 'title': category.name[language], 'is_completed': my_request.is_completed,
                    'request_id': my_request._id, 'expiry_text': 'Expires in 7 days'}

    return request_data


def request_json_for_workrequest(work_request, language, questions_dict):
    user = User.objects.get(_id=work_request.user_id)
    request_data = {'req_id': work_request._id, 'reqby_name': user.name, 'reqby_rating': user.rating,
                    'loc_name': work_request.location, "mobile": user.mobile}
    # add req_summary
    request_data['work'] = get_questions(work_request.questions, questions_dict, language)
    if user.pic_url:
        request_data['reqby_img'] = user.pic_url
    elif user.aud_url:
        request_data['aud_url'] = user.aud_url
    # add time if it is created today otherwise send date
    get_date = convert_timestamps(work_request.created_at)
    request_data['created_at'] = str(get_date.day) + ' ' + str(get_month[get_date.month][language])
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
        body['to'] = user.fcm_token
        body['data']['title'] = '{} from {} requested for your service'.format(user.name, location_name)
        requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=body)


def categories_dict(categories_list):
    request_dict = {}
    for category in categories_list:
        request_dict[category.id] = category
    return request_dict


def today_date():
    today = datetime.now()
    today_timestamp = datetime.timestamp(today)
    return date.fromtimestamp(today_timestamp)


def convert_timestamps(timestmp):
    return date.fromtimestamp(timestmp)


def my_requests_list_func(fetched_requests, categories, language):
    ongoing_requests = []
    other_requests = []

    if len(fetched_requests):
        header_for_ongoing_requests(ongoing_requests, language)

        for request in fetched_requests:

            get_date = convert_timestamps(request.created_at)
            diff = get_date - today_date()

            request_obj = request_json_for_myrequest(request, categories[request.category_id], language)
            request_obj['subtitle'] = str(get_date.day) + ' ' + str(get_month[get_date.month][language])

            if diff.days <= 7 and (request.is_completed == False):
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
    request_data = {'name': user.name, 'user_id': user._id, 'mobile': user.mobile}
    if user.pic_url:
        request_data['pic_url'] = user.pic_url
    return request_data


def get_provider_details(users_list):
    providers_list = []
    for user in users_list:
        user_obj = request_json_for_user(user)
        providers_list.append(user_obj)
    return providers_list
