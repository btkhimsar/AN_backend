import json
from datetime import datetime
from http import HTTPStatus

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.location import DISTANCE
from Constants.response_strings import *
from setup import client
from users.models import User
from util.response import create_resp_dict
from .models import Request
from .utility import create_point_dict, request_json


@api_view(['GET'])
def work_requests(request):
    if request.method == 'GET':
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
                # print(location.latitude)
                resp_data = create_resp_dict(True, WORK_REQUEST_FETCHED)
                resp_data['workrequests'] = []
                workrequests = Request.objects(
                    location__geo_within_center=[(location['latitude'], location['longitude']), DISTANCE])
                for i in workrequests:
                    resp_data['workrequests'].append(request_json(i))
                    print(i)
                resp_data['location_text'] = LOCATIONS_TEXT
                resp_data['location_subtext'] = LOCATIONS_SUBTEXT
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def my_request(request):
    if request.method == 'GET':
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
                    ret.append(request_json(i))
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
                comment = body_data['comments']
                print(user_id)
                customer = User.objects(id=user_id).first()
                location = body_data['location']
                location = create_point_dict(location['latitude'], location['longitude'])
                category_id = body_data['category_id']
                print(location)
                creation_date = datetime.utcnow()
                request = Request(category_id=category_id, location=location, user_id=user_id,
                                  creation_date=creation_date, title="Request by {}".format(customer.name),
                                  mobile=customer.mobile)
                if comment is not None:
                    request['comments'] = comment
                request.save()
                resp_data = create_resp_dict(True, REQUEST_CREATED)
                resp_data['requestId'] = str(request.id)
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
