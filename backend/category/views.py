import json
from http import HTTPStatus

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.response_strings import SUBCATEGORY_ADDED, CATEGORY_ADDED, DATA_FETCHED, INCORRECT_REQUEST
from setup import client
from util.response import create_resp_dict
from .constants import data
from .models import SubCategory, Category


@api_view(['GET'])
def category_list(request):
    # todo change dummy data to format as per contract
    if request.method == 'GET':
        return JsonResponse(data=data, safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def handle_subcategory(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                category_id = body_data['category_id']
                super_category_id = body_data['super_category_id']
                description = body_data['description']
                img_url = body_data['img_url']
                categorytype = body_data['type']
                tg = body_data['tg']
                subcategory = SubCategory(category_id=category_id, super_category_id=super_category_id,
                                          description=description, img_url=img_url, type=categorytype, tg=tg)
                subcategory.save()
                return JsonResponse(data=create_resp_dict(True, SUBCATEGORY_ADDED), safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def handle_category(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                name = body_data['name']
                super_category_id = body_data['super_category_id']
                description = body_data['description']
                img_url = body_data['img_url']
                category = Category(name=name, super_category_id=super_category_id,
                                    description=description, img_url=img_url)
                category.save()
                return JsonResponse(data=create_resp_dict(True, CATEGORY_ADDED), safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['GET'])
def show_categories(request):
    # todo make sure to divert the category list api to this one
    if request.method == 'GET':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                # todo write logic to create a catgory list response as req
                return JsonResponse(data=create_resp_dict(True, DATA_FETCHED), safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)
