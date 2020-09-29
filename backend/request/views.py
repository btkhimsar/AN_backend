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
from .constants import *


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
                language = body_data['language']
                page_no = body_data['page_no']

                offset = (page_no-1) * requests_per_page

                user = User.objects.get(id=user_id)
                workrequests = Request.objects(location__geo_within_center=[(location['latitude'],
                                            location['longitude']), radius], category_id__in=user.provider_info.category,
                                               is_completed=False).order_by('-created_at').skip(offset).limit(requests_per_page)
                questions_list = Question.objects
                questions_dict = get_questions_dict(questions_list)

                resp_data = create_resp_dict(True, WORK_REQUEST_FETCHED)
                resp_data['location_text'] = location_text(language, len(workrequests))
                resp_data['loc_img'] = ""
                resp_data['work_img'] = ""
                resp_data['workrequests'] = work_requests_list(workrequests, language, questions_dict)

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
                language = body_data['language']

                my_requests_list = Request.objects(user_id=user_id).order_by('-created_at')
                categories_list = Category.objects

                fetched_categories_dict = categories_dict(categories_list)

                resp_data = create_resp_dict(True, REQUEST_FETCHED)

                fetched_my_requests = my_requests_list_func(fetched_requests=my_requests_list, categories=fetched_categories_dict,
                                                            language=language)

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
                location_name = body_data['location_name']
                questions = body_data['questions']
                aud_url = body_data['aud_url']
                share_mobile = body_data['share_mobile']

                customer = User.objects.get(id=user_id)

                category = Category.objects.get(id=category_id)

                providers_list = User.objects(user_type='provider')
                users_list = providers_list(provider_info__loc__geo_within_center=
                                            [(location['latitude'], location['longitude']), 0.095],
                                         provider_info__category=category_id, provider_info__is_active=True)

                point = create_point_dict(location['latitude'], location['longitude'])
                request = Request(category_id=category_id, location=point, user_id=user_id, location_name=location_name,
                                 share_mobile=share_mobile)

                resp_data = create_resp_dict(True, REQUEST_CREATED)
                if comment:
                    request['comment'] = comment
                if questions:
                    for ques_id in questions:
                        request['questions'][ques_id] = questions[ques_id]
                if aud_url:
                    request['aud_url'] = aud_url
                request.save()
                customer.my_requests.append(str(request.id))
                customer.save()

                notification(users_list, location_name)

                resp_data['requestId'] = str(request.id)
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)
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
                completed_by = body_data['completed_by']

                request = Request.objects.get(id=request_id)
                user = User.objects.get(id=completed_by)

                request.completed_by = completed_by
                request.is_completed = True
                request.save()
                return JsonResponse(data=create_resp_dict(True, "Request Completed"), safe=False,
                                    status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def send_interest(request):
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

                request = Request.objects.get(id=request_id)
                provider = User.objects.get(id=user_id)
                consumer = User.objects.get(id=request.user_id)

                request.interested_users.append(user_id)
                request.new_interest_count += 1
                request.save()

                provider.provider_info.sent_interests.append(request_id)
                provider.save()

                notification_to_consumer(consumer, provider)

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
                language = body_data['language']

                request = Request.objects.get(id=request_id)
                users_list = User.objects(id__in=request.interested_users)
                category = Category.objects.get(id=request.category_id)
                fetched_questions = Question.objects
                get_date = datetime.now()

                questions_dict = get_questions_dict(fetched_questions)

                request.new_interest_count = 0
                request.save()

                resp = create_resp_dict(True, "Details Fetched")
                resp['title'] = "For {}".format(category.name[language])
                resp['subtitle'] = str(get_date.day) + ' ' + str(get_month[get_date.month][language])
                resp['work'] = get_questions(request.questions, questions_dict, language)
                resp['aud_url'] = request.aud_url
                resp['interested_users_text'] = "Interested {} ({})".format(category.name[language],
                                                                            len(request.interested_users))
                resp['interested_users'] = get_provider_details(users_list)
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def interests_sent(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                language = body_data['language'].lower()

                user = User.objects.get(id=user_id)
                requests_list = Request.objects(id__in=user.provider_info.sent_interests)
                questions_list = Question.objects

                questions_dict = get_questions_dict(questions_list)

                resp = create_resp_dict(True, WORK_REQUEST_FETCHED)
                resp['interests_sent'] = work_requests_list(requests_list, language, questions_dict)

                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@token_required
def mark_as_spam(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                auth_token = body_data['auth_token']
                user_id = body_data['user_id']
                provider_id = body_data['provider_id']
                request_id = body_data['request_id']

                provider = User.objects.get(id=provider_id)
                request = Request.objects.get(id=request_id)

                provider.provider_info.complaints_count += 1
                provider.save()

                request.complaints_count += 1
                request.save()

                return JsonResponse(data=create_resp_dict(True, "Marked As Spam"), safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)