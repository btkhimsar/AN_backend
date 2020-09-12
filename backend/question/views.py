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

                question = Question(question_type=question_type, isMandatory=isMandatory)
                for i in text:
                    question.text[i] = text[i]
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
                answer_id = body_data['answer_id']
                text = body_data['text']
                question_id = body_data['question_id']

                question = Question.objects.get(id=question_id)
                answer = Answer(answer_id=answer_id)

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
                sub_question_id = body_data['sub_question_id']
                sub_question_type = body_data['sub_question_type']
                text = body_data['text']
                isMandatory = body_data['isMandatory']
                answer_id = body_data['answer_id']
                question_id = body_data['question_id']

                question = Question.objects.get(id=question_id)
                answer = question.answers.filter(answer_id=answer_id)[0]
                sub_question = SubQuestion(sub_question_id=sub_question_id, sub_question_type=sub_question_type,
                                           isMandatory=isMandatory)

                for language in text:
                    sub_question.text[language] = text[language]
                answer.sub_questions.append(sub_question)
                question.save()
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
                sub_answer_id = body_data['sub_answer_id']
                text = body_data['text']
                sub_question_id = body_data['sub_question_id']
                answer_id = body_data['answer_id']
                question_id = body_data['question_id']

                question = Question.objects.get(id=question_id)
                answer = question.answers.filter(answer_id=answer_id)[0]
                sub_question = answer.sub_questions.filter(sub_question_id=sub_question_id)[0]
                sub_answer = SubAnswer(sub_answer_id=sub_answer_id)

                for language in text:
                    sub_answer.text[language] = text[language]
                sub_question.sub_answers.append(sub_answer)
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
                user_language = body_data['user_language']

                category = Category.objects.get(id=category_id)
                questions_list = Question.objects

                questions_dict = questions_dict_func(questions_list)

                resp_data = create_resp_dict(True, QUESTION_FETCHED)
                resp_data['questions_list'] = questions_list_func(questions_dict, category, user_language)
                return JsonResponse(data=resp_data, safe=False, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse(data=create_resp_dict(False, e), safe=False,
                                    status=HTTPStatus.OK)

