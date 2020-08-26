import json
from http import HTTPStatus

from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from Constants.response_strings import *
from setup import client
from util.response import create_resp_dict
from .constants import data
from .models import Category, SuperCategory, Question, Answer, SubQuestion, SubAnswer
from .helpers import request_json, request_json_for_question


@api_view(['POST'])
def super_category_list(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8'))==0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                user_language = body_data['user_language'].lower()
                user_type = body_data['user_type'].lower()
                list = SuperCategory.objects
                if len(list)!=0:
                    super_categories = []
                    for i in list:
                        temp = request_json(request=i, user_language=user_language)
                        super_categories.append(temp)
                    resp = create_resp_dict(True, DATA_FETCHED)
                    resp['super_categories'] = super_categories
                    return JsonResponse(data=resp, safe=True, status=HTTPStatus.OK)
                return JsonResponse(data=create_resp_dict(False, NO_CATEGORY), safe=False, status=HTTPStatus.OK)
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
                body_data = json.loads(request.body.decode('utf-8'))
                category_id = body_data['category_id']
                name = body_data['name']
                description = body_data['description']
                icon_url = body_data['icon_url']
                has_questions = body_data['has_questions']
                new_category = Category(icon_url=icon_url, has_questions=has_questions)
                for i in name:
                    new_category.name[i] = name[i]
                for j in description:
                    new_category.description[j] = description[j]
                new_category.save()
                resp = create_resp_dict(True, SUBCATEGORY_ADDED)
                resp['category_id'] = str(new_category.id)
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)


@api_view(['POST'])
def handle_super_category(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                print(client)
                body_data = json.loads(request.body.decode('utf-8'))
                name = body_data['name']
                description = body_data['description']
                default_view_count = body_data['default_view_count']
                category = SuperCategory()
                for i in name:
                    category.name[i] = name[i]
                for j in description:
                    category.description[j] = description[j]
                category.default_view_count = default_view_count
                category.save()
                resp = create_resp_dict(True, CATEGORY_ADDED)
                return JsonResponse(data=resp, safe=False, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False, status=HTTPStatus.OK)

@api_view(['POST'])
def add_question(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8'))==0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                type = body_data['type']
                text = body_data['text']
                isMandatory = body_data['isMandatory']
                question = Question(type=type, isMandatory=isMandatory)
                for i in text:
                    question.text[i] = text[i]
                question.save()
                return JsonResponse(data=create_resp_dict(True, QUESTION_CREATED), safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)

@api_view(['POST'])
def questions_list(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8'))==0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                category_id = body_data['category_id']
                user_language = body_data['user_language']
                category = Category.objects.get(id=category_id)
                questions_list = []
                for i in category.questions:
                    questions_list.append(request_json_for_question(i, user_language))
                resp_data = create_resp_dict(True, QUESTION_FETCHED)
                resp_data['questions_list'] = questions_list
                return JsonResponse(data=resp_data, safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)

@api_view(['POST'])
def add_answer(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8'))==0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                answer_id = body_data['answer_id']
                text = body_data['text']
                question_id = body_data['question_id']
                question = Question.objects.get(id=question_id)
                answer = Answer(answer_id=answer_id)
                for i in text:
                    answer.text[i] = text[i]
                question.answers.append(answer)
                question.save()
                return JsonResponse(data=create_resp_dict(True, ANSWER_ADDED), safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)

@api_view(['POST'])
def add_sub_question(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                sub_question_id = body_data['sub_question_id']
                type = body_data['type']
                text = body_data['text']
                isMandatory = body_data['isMandatory']
                answer_id = body_data['answer_id']
                question_id = body_data['question_id']
                question = Question.objects.get(id=question_id)
                answer = question.answers.filter(answer_id=answer_id)[0]
                sub_question = SubQuestion(sub_question_id=sub_question_id, type=type, isMandatory=isMandatory)
                for i in text:
                    sub_question.text[i] = text[i]
                answer.sub_questions.append(sub_question)
                question.save()
                return JsonResponse(data=create_resp_dict(True, ANSWER_ADDED), safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)

@api_view(['POST'])
def add_sub_answer(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                sub_answer_id = body_data['sub_answer_id']
                text = body_data['text']
                sub_question_id = body_data['sub_question_id']
                answer_id = body_data['answer_id']
                question_id = body_data['question_id']
                question = Question.objects.get(id=question_id)
                answer = question.answers.filter(answer_id=answer_id)[0]
                sub_question = answer.sub_questions.filter(sub_question_id=sub_question_id)[0]
                sub_answer = SubAnswer(sub_answer_id=sub_answer_id)
                for i in text:
                    sub_answer.text[i] = text[i]
                sub_question.sub_answers.append(sub_answer)
                question.save()
                return JsonResponse(data=create_resp_dict(True, ANSWER_ADDED), safe=False,
                                    status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)