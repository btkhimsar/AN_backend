import json
from datetime import datetime
from http import HTTPStatus

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.response_strings import *
from setup import client
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
                radius_in_km = body_data['radius']
                radius_in_radian = radius_in_km/6378
                # print(radius_in_radian)
                resp_data = create_resp_dict(True, WORK_REQUEST_FETCHED)
                resp_data['workrequests'] = []
                user = User.objects(id=user_id).first()
                # print(user.work_category)
                workrequests = Request.objects(
                    location__geo_within_center=[(location['latitude'], location['longitude']), radius_in_radian], category_id=user.work_category)
                for i in workrequests:
                    user = User.objects(id=i.user_id).first()
                    workrequest = request_json_for_workrequests(i)
                    workrequest['title'] = 'Request from {}'.format(user.name)
                    resp_data['workrequests'].append(workrequest)
                resp_data['location_text'] = LOCATIONS_TEXT
                resp_data['location_subtext'] = LOCATIONS_SUBTEXT
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
                ret = []
                user_id = body_data['user_id']
                request = Request.objects(user_id=user_id)
                resp_data = create_resp_dict(True, REQUEST_FETCHED)
                for i in request:
                    temp = request_json_for_myrequests(i)
                    # how to fetch all the categories with particular category_id
                    ret.append(temp)
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
                radius = body_data['radius']
                location = body_data['location']
                category_id = body_data['category_id']
                customer = User.objects(id=user_id).first()
                location = create_point_dict(location['latitude'], location['longitude'])
                created_at = datetime.utcnow()
                request = Request(category_id=category_id, location=location, user_id=user_id,
                                  created_at=created_at, mobile=customer.mobile, radius=radius)
                if comment is not None:
                    request['comment'] = comment
                request.save()
                resp_data = create_resp_dict(True, REQUEST_CREATED)
                resp_data['requestId'] = str(request.id)
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
