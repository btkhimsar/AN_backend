import json
from http import HTTPStatus
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from Constants.response_strings import *
from util.response import create_resp_dict
from .models import *
from .utility import *
from category.models import Category


@api_view(['POST'])
def add_question(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                question_type = body_data['question_type']
                text = body_data['text']
                isMandatory = body_data['isMandatory']

                question = Question(question_type=question_type, isMandatory=isMandatory,
                                    _id=Question.objects.count()+1)
                for language in text:
                    question.text[language] = text[language]
                question.save()
                return JsonResponse(data=create_resp_dict(True, QUESTION_CREATED), safe=False,
                                    status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)


@api_view(['POST'])
def add_answer(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                text = body_data['text']
                qId = body_data['qId']

                question = Question.objects.get(_id=qId)
                answer = Answer()

                for language in text:
                    answer.text[language] = text[language]
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
                question_type = body_data['question_type']
                text = body_data['text']
                isMandatory = body_data['isMandatory']
                aId = body_data['aId']
                qId = body_data['qId']

                question = Question.objects.get(_id=qId)
                answer = question.answers.filter(ans_id=aId)[0]
                sub_question = Question(question_type=question_type, isMandatory=isMandatory,
                                        _id=Question.objects.count()+1)

                for language in text:
                    sub_question.text[language] = text[language]
                answer.questions.append(sub_question._id)
                question.save()
                sub_question.save()
                return JsonResponse(data=create_resp_dict(True, SUBQUESTION_ADDED), safe=False,
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
                text = body_data['text']
                qId = body_data['qId']

                question = Question.objects.get(_id=qId)
                sub_answer = Answer()

                for language in text:
                    sub_answer.text[language] = text[language]
                question.answers.append(sub_answer)
                question.save()
                return JsonResponse(data=create_resp_dict(True, SUBANSWER_ADDED), safe=False,
                                    status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)


@api_view(['POST'])
def questions(request):
    if request.method == 'POST':
        if request.body is None or len(request.body.decode('utf-8')) == 0:
            return JsonResponse(data=create_resp_dict(False, INCORRECT_REQUEST), safe=False,
                                status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                category_id = body_data['category_id']
                language = body_data['language']

                category = Category.objects.get(_id=category_id)
                questions_list = Question.objects

                questions_dict = questions_dict_func(questions_list)

                resp_data = create_resp_dict(True, QUESTION_FETCHED)
                questions_list_func(questions_dict, category, language, resp_data)
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)

