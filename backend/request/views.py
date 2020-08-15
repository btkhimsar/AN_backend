import json
from datetime import datetime, date
from http import HTTPStatus

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.response_strings import *
from setup import client
from category.models import Category, SuperCategory
from users.models import User
from util.response import create_resp_dict
from .models import Request
from .utility import create_point_dict, request_json_for_myrequests, request_json_for_workrequests


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
                resp_data = create_resp_dict(True, WORK_REQUEST_FETCHED)
                ret = []
                user = User.objects.get(id=user_id)
                work_category = user.work_category
                user_language = user.user_language
                category = Category.objects.get(id=work_category)
                workrequests = Request.objects(
                    location__geo_within_center=[(location['latitude'], location['longitude']), radius], category_id=work_category)
                timestamp = date.fromtimestamp(datetime.timestamp(datetime.now()))
                if user_language=='english':
                    ret.append({'title': 'Today', 'type': 'header'})
                elif user_language=='hindi':
                    ret.append({'title': 'आज', 'type': 'header'})
                number_of_workrequests = len(workrequests)
                j = 0
                for i in range(number_of_workrequests):
                    if date.fromtimestamp(workrequests[i].created_at) == timestamp:
                        ret.append(request_json_for_myrequests(workrequests[i]))
                        j = i
                    else:
                        break
                if user_language=='english':
                    ret.append({'title': '120 other requests already completed', 'type': 'footer'})
                elif user_language=='hindi':
                    ret.append({'title': '120 अन्य अनुरोध पहले ही पूरे हो चुके हैं', 'type': 'footer'})
                if user_language=='english':
                    ret.append({'title': '1 day ago', 'type': 'header'})
                elif user_language=='hindi':
                    ret.append({'title': '1 दिन पहले', 'type': 'header'})
                for k in range(j + 1, number_of_workrequests):
                    ret.append(request_json_for_myrequests(workrequests[k]))
                if user_language=='english':
                    ret.append({'title': '120 other requests already completed', 'type': 'footer'})
                elif user_language=='hindi':
                    ret.append({'title': '120 अन्य अनुरोध पहले ही पूरे हो चुके हैं', 'type': 'footer'})
                if user_language=='english':
                    resp_data['location_text'] = "{} active requests for {} near".format(number_of_workrequests, category.name[user_language])
                elif user_language=='hindi':
                    resp_data['location_text'] = "निकट {} के लिए {} सक्रिय कार्य अनुरोध".format(category.name[user_language], number_of_workrequests)
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
                timestamp = date.fromtimestamp(datetime.timestamp(datetime.now()))
                requests = Request.objects(user_id=user_id)
                resp_data = create_resp_dict(True, REQUEST_FETCHED)
                ret.append({'title': 'Today', 'type': 'header'})
                number_of_requests = len(requests)
                j = 0
                for i in range(number_of_requests):
                    if date.fromtimestamp(requests[i].created_at) == timestamp:
                        ret.append(request_json_for_myrequests(requests[i]))
                        j=i
                    else:
                        break
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
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                # todo verify auth token
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                comment = body_data['comment']
                location = body_data['location']
                category_id = body_data['category_id']
                super_category_id = body_data['super_category_id']
                location_name = body_data['location_name']
                customer = User.objects.get(id=user_id)
                category = Category.objects.get(id=category_id)
                super_category = SuperCategory.objects.get(id=super_category_id)
                location = create_point_dict(location['latitude'], location['longitude'])
                request = Request(category_id=category_id, location=location, user_id=user_id,
                                  mobile=customer.mobile, location_name=location_name, super_category_id=super_category_id)
                now = datetime.now()
                request['created_at'] = datetime.timestamp(now)
                if comment is not None:
                    request['comment'] = comment
                request.save()
                resp_data = create_resp_dict(True, REQUEST_CREATED)
                resp_data['requestId'] = str(request.id)
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
