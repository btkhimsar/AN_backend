import json
from datetime import datetime, date
from http import HTTPStatus
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from Constants.response_strings import *
from category.models import Category, SuperCategory
from users.models import User
from util.response import create_resp_dict, token_required
from .models import Request
from .utility import *
from question.models import Question


@api_view(['POST'])
@token_required
def work_requests(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                location = body_data['location']
                radius = body_data['radius']/105
                user_language = body_data['user_language']

                user = User.objects.get(_id=user_id)
                category = Category.objects.get(id=user.work_category)
                workrequests = Request.objects(location__geo_within_center=[(location['latitude'],
                                            location['longitude']), radius], category_id=user.work_category,
                                               isCompleted=False).order_by('-created_at')

                resp_data = create_resp_dict(True, WORK_REQUEST_FETCHED)
                resp_data['location_text'] = location_text(user_language, len(workrequests), category)
                resp_data['location_icon_url'] = ""
                resp_data['work_icon_url'] = ""
                resp_data['workrequests'] = work_requests_list(workrequests, user_language)

                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def my_requests(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                user_language = body_data['user_language']

                requests_ids = User.objects.get(_id=user_id).interests
                my_requests_list = Request.objects(_id__in=requests_ids).order_by('-created_at')
                categories_list = Category.objects

                fetched_categories_dict = categories_dict(categories_list)

                resp_data = create_resp_dict(True, REQUEST_FETCHED)

                fetched_my_requests = my_requests_list_func(fetched_requests=my_requests_list, categories=fetched_categories_dict,
                                                            user_language=user_language)

                resp_data['myrequests'] = fetched_my_requests

                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def create_request(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                comment = body_data['comment']
                location = body_data['location']
                category_id = body_data['category_id']
                super_category_id = body_data['super_category_id']
                location_name = body_data['location_name']
                questions = body_data['questions']
                aud_url = body_data['aud_url']

                customer = User.objects.get(_id=user_id)

                category = Category.objects.get(id=category_id)
                super_category = SuperCategory.objects.get(id=super_category_id)

                users_list = User.objects(base_location__geo_within_center=[(location['latitude'],
                                        location['longitude']), 0.095], user_type='provider',
                                         work_category=category_id, active=True)

                location = create_point_dict(location['latitude'], location['longitude'])
                request = Request(category_id=category_id, location=location, user_id=user_id, mobile=customer.mobile,
                                  location_name=location_name, super_category_id=super_category_id, _id=Request.objects.count()+1)

                now = datetime.now()
                request['created_at'] = datetime.timestamp(now)

                if comment is not None:
                    request['comment'] = comment
                if questions:
                    for question in questions:
                        request['questions'].append(question)
                if aud_url:
                    request['aud_url'] = aud_url
                request.save()
                customer.interests.append(request._id)
                customer.save()

                notification(users_list, location_name)

                resp_data = create_resp_dict(True, REQUEST_CREATED)
                resp_data['requestId'] = str(request._id)
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
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
                request = Request.objects.get(_id=request_id, user_id=user_id)
                request.isCompleted = isCompleted
                request.save()
                return JsonResponse(data=create_resp_dict(True, REQUEST_UPDATED), safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def request_completion(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                request_id = body_data['request_id']
                provider_id = body_data['provider_id']

                request = Request.objects.get(_id=request_id)

                request.provider_id = provider_id
                request.save()
                return JsonResponse(data=create_resp_dict(True, "Request Completed"), safe=False,
                                    status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def send_interest(request):
    print("working")
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                print(user_id)
                request_id = body_data['request_id']
                print(request_id)
                request = Request.objects.get(_id=request_id)
                print(request)
                request.interested_users.append(user_id)
                request.save()
                return JsonResponse(data=create_resp_dict(True, "Interest Sent"), safe=False,
                                    status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def my_request_details(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                request_id = body_data['request_id']
                user_language = body_data['user_language']

                request = Request.objects.get(_id=request_id)
                users_list = User.objects(_id__in=request.interested_users)
                category = Category.objects.get(id=request.category_id)
                fetched_questions = Question.objects
                get_date = today_date()

                questions_dict = get_questions_dict(fetched_questions)

                resp = create_resp_dict(True, "Details Fetched")
                resp['title'] = "For {}".format(category.name[user_language])
                resp['subtitle'] = str(get_date.day) + ' ' + str(get_month[get_date.month][user_language])
                resp['work'] = get_questions(request.questions, questions_dict, user_language)
                resp['aud_url'] = request.aud_url
                resp['interested_users_text'] = "Interested {} ({})".format(category.name[user_language],
                                                                            len(request.interested_users))
                resp['interested_users'] = get_user_details(users_list)
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)