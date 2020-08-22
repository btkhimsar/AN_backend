import json
from datetime import datetime, date
from http import HTTPStatus
import requests

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.response_strings import *
from setup import client
from category.models import Category, SuperCategory
from users.models import User
from util.response import create_resp_dict
from .models import Request, Question
from .utility import create_point_dict, request_json_for_myrequests, request_json_for_workrequests, \
    header_for_today, header_for_1dayago, footer_for_today, footer_for_1dayago, location_text
from .constants import body, headers

@api_view(['POST'])
def work_requests(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                # todo verify auth token
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                location = body_data['location']
                radius = body_data['radius']/105
                user_language = body_data['user_language']
                resp_data = create_resp_dict(True, WORK_REQUEST_FETCHED)
                ret = []
                user = User.objects.get(id=user_id)
                category = Category.objects.get(id=user.work_category)
                total_workrequests = Request.objects
                workrequests = Request.objects(
                    location__geo_within_center=[(location['latitude'], location['longitude']), radius], category_id=user.work_category, isCompleted=False, isExpired=False)
                number_of_workrequests = len(workrequests)
                if (number_of_workrequests):
                    header_for_today(ret, user_language)
                    j=0
                    timestamp = date.fromtimestamp(datetime.timestamp(datetime.now()))
                    for i in range(number_of_workrequests):
                        if date.fromtimestamp(workrequests[i].created_at) == timestamp:
                            ret.append(request_json_for_workrequests(workrequests[i]))
                            j = i
                        else:
                            break
                    footer_for_today(ret, user_language)
                if (j<number_of_workrequests-1):
                    header_for_1dayago(ret, user_language)
                    for k in range(j + 1, number_of_workrequests):
                        ret.append(request_json_for_workrequests(workrequests[k]))
                    footer_for_1dayago(ret, user_language)
                resp_data['location_text'] = location_text(user_language, len(total_workrequests)-number_of_workrequests, category)
                resp_data['location_subtext'] = LOCATIONS_SUBTEXT
                resp_data['workrequests'] = ret
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def my_request(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                # todo verify auth token
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                ret = []
                requests = Request.objects(user_id=user_id)
                user = User.objects.get(id=user_id)
                resp_data = create_resp_dict(True, REQUEST_FETCHED)
                number_of_requests = len(requests)
                if number_of_requests:
                    header_for_today(ret, user.user_language)
                    j = 0
                    timestamp = date.fromtimestamp(datetime.timestamp(datetime.now()))
                    for i in range(number_of_requests):
                        if date.fromtimestamp(requests[i].created_at) == timestamp:
                            ret.append(request_json_for_myrequests(requests[i]))
                            j=i
                        else:
                            break
                if j<number_of_requests-1:
                    ret.append({'title': '1 day ago', 'type': 'header'})
                    for k in range(j+1, number_of_requests):
                        ret.append(request_json_for_myrequests(requests[k]))
                resp_data['myrequests'] = ret
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def job(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                # todo verify auth token
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                comment = body_data['comment']
                location = body_data['location']
                category_id = body_data['category_id']
                super_category_id = body_data['super_category_id']
                location_name = body_data['location_name']
                questions = body_data['questions']
                customer = User.objects.get(id=user_id)
                category = Category.objects.get(id=category_id)
                super_category = SuperCategory.objects.get(id=super_category_id)
                users = User.objects(
                    base_location__geo_within_center=[(location['latitude'], location['longitude']), 0.095],
                    user_type='provider', work_category=category_id, active=True)
                location = create_point_dict(location['latitude'], location['longitude'])
                request = Request(category_id=category_id, location=location, user_id=user_id,
                                  mobile=customer.mobile, location_name=location_name, super_category_id=super_category_id)
                now = datetime.now()
                request['created_at'] = datetime.timestamp(now)
                if comment is not None:
                    request['comment'] = comment
                for i in range(len(questions)):
                    each_question = Question(qId=questions[i]['qId'])
                    if "remarks" in questions[i]:
                        each_question['remarks'] = questions[i]['remarks']
                    for j in questions[i]['aId']:
                        each_question.aId.append(j)
                    request.questions.append(each_question)
                request.save()
                resp_data = create_resp_dict(True, REQUEST_CREATED)
                resp_data['requestId'] = str(request.id)
                for user in users:
                    body['to'] = user.token
                    body['notification']['body'] = '{} from {} requested for your service'.format(user.name, location_name)
                    temp = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=body)
                resp_data['notification'] = "Notification sent successfully to all the providers within a range of 10 kms"
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def my_request_update(request):
    if request.method=='POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                request_id = body_data['request_id']
                isCompleted = body_data['isCompleted']
                request = Request.objects.get(id=request_id, user_id=user_id)
                request.isCompleted = isCompleted
                request.save()
                return JsonResponse(data=create_resp_dict(True, REQUEST_UPDATED), safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
