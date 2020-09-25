import json
from http import HTTPStatus

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.response_strings import *
from languages.models import Language
from setup import client
from util.response import create_resp_dict
from .constants import data

@api_view(['POST'])
def add_language(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                language_data = body_data['language_data']
                for data in language_data:
                    lang = Language.objects(text=data['text']).first()
                    lang.update(**data).save()
                return JsonResponse(data=create_resp_dict(True, LANGUAGE_ADDED), safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def create_language(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                language_data = body_data['language_data']
                for data in language_data:
                    Language(text=data['text'], english=data['english']).save()

                return JsonResponse(data=create_resp_dict(True, CATEGORY_ADDED), safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)

@api_view(['POST'])
def language_data(request):
    if request.method == 'POST':
        if request.body is None and len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                language = body_data['language'].lower()
                if language == 'english':
                    resp = create_resp_dict(True, DATA_FETCHED)
                    resp['language'] = data['english']
                elif language == 'hindi':
                    resp = create_resp_dict(True, DATA_FETCHED)
                    resp['language'] = data['hindi']
                else:
                    resp = create_resp_dict(False, "No Strings Available")
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK )
