from Constants.image_urls import HOME_ICON
import requests
from .constants import body, headers
from datetime import datetime, date
from users.models import User


def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point


def request_json_for_myrequest(my_request, category, super_category, user_language):
    request_data = {'subtitle': '{} > {}'.format(super_category.name[user_language],
                    category.name[user_language]), 'isCompleted': my_request.isCompleted,
                    'request_id': str(my_request.id)}
    if user_language == 'english':
        request_data['title'] = "You requested for"
    elif user_language == 'hindi':
        request_data['title'] = 'आपने निवेदन किया'
    return request_data


def request_json_for_workrequest(work_request):
    user_name = User.objects.get(id=work_request.user_id).name
    request_data = {'title': 'Request from {}'.format(user_name), 'subtitle': work_request.location_name,
                    'subtitle_icon': HOME_ICON, 'mobile': work_request.mobile, 'type': 'request',
                    'request_id': str(work_request.id), 'questions': []}
    return request_data


def header_for_today(work_request_list, language):
    if language == 'english':
        work_request_list.append({'title': 'Today', 'type': 'header'})
    elif language == 'hindi':
        work_request_list.append({'title': 'आज', 'type': 'header'})


def footer_for_today(work_request_list, language):
    if language == 'english':
        work_request_list.append({'title': '120 other requests already completed', 'type': 'footer'})
    elif language == 'hindi':
        work_request_list.append({'title': '120 अन्य अनुरोध पहले ही पूरे हो चुके हैं', 'type': 'footer'})


def header_for_1dayago(work_request_list, language):
    if language == 'english':
        work_request_list.append({'title': '1 day ago', 'type': 'header'})
    elif language == 'hindi':
        work_request_list.append({'title': '1 दिन पहले', 'type': 'header'})


def footer_for_1dayago(work_request_list, language):
    if language == 'english':
        work_request_list.append({'title': '120 other requests already completed', 'type': 'footer'})
    elif language == 'hindi':
        work_request_list.append({'title': '120 अन्य अनुरोध पहले ही पूरे हो चुके हैं', 'type': 'footer'})


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


def my_requests_list_func(fetched_requests, categories, super_categories, user_language):
    requests_list = []
    total_requests = len(fetched_requests)
    requests_count = 0
    remaining_requests = 0
    if total_requests:
        header_for_today(requests_list, user_language)
        for request in fetched_requests:
            if date.fromtimestamp(request.created_at) == today_date():
                request_obj = request_json_for_myrequest(request, categories[request.category_id],
                                                         super_categories[request.super_category_id], user_language)
                requests_list.append(request_obj)
                requests_count += 1
                remaining_requests = requests_count
            else:
                break

    if remaining_requests < (total_requests-1):
        header_for_1dayago(requests_list, user_language)
        for count in range(remaining_requests+1, total_requests):
            request_obj = request_json_for_myrequest(fetched_requests[count], categories[fetched_requests[count].category_id],
                                                     super_categories[fetched_requests[count].super_category_id], user_language)
            requests_list.append(request_obj)
    return requests_list


def work_requests_list(fetched_requests, user_language):
    requests_list = []
    total_requests = len(fetched_requests)
    requests_count = 0
    remaining_requests = 0
    if total_requests:
        header_for_today(requests_list, user_language)
        for request in fetched_requests:
            if date.fromtimestamp(request.created_at) == today_date():
                request_obj = request_json_for_workrequest(request)
                requests_list.append(request_obj)
                requests_count += 1
                remaining_requests = requests_count
            else:
                break
        footer_for_today(requests_list, user_language)
    if remaining_requests < (total_requests - 1):
        header_for_1dayago(requests_list, user_language)
        for count in range(remaining_requests + 1, total_requests):
            request_obj = request_json_for_workrequest(fetched_requests[count])
            requests_list.append(request_obj)
        footer_for_1dayago(requests_list, user_language)
    return requests_list
