import json
from http import HTTPStatus
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from Constants.response_strings import *
from util.response import create_resp_dict
from .models import *
from .helpers import *


@api_view(['POST'])
def categories(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                user_language = body_data['user_language'].lower()

                super_categories_list = SuperCategory.objects
                categories_list = Category.objects

                fetched_categories_dict = categories_dict(categories_list)

                super_categories = []
                for super_category in super_categories_list:
                    super_category_in_json = request_json(super_category, fetched_categories_dict, user_language)
                    super_categories.append(super_category_in_json)

                resp = create_resp_dict(True, DATA_FETCHED)
                resp['super_categories'] = super_categories
                return JsonResponse(data=resp, safe=False)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def create_category(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                name = body_data['name']
                icon_url = body_data['icon_url']
                new_category = Category(icon_url=icon_url)
                for language in name:
                    new_category.name[language] = name[language]
                new_category.save()
                resp = create_resp_dict(True, SUBCATEGORY_ADDED)
                resp['category_id'] = str(new_category.id)
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def create_super_category(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                name = body_data['name']
                default_view_count = body_data['default_view_count']
                new_super_category = SuperCategory(default_view_count=default_view_count)
                for language in name:
                    new_super_category.name[language] = name[language]
                new_super_category.save()
                resp = create_resp_dict(True, CATEGORY_ADDED)
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


