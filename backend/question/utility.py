def question_json(ques_obj, user_language):
    request_data = {'question_id': str(ques_obj.id), 'question_type': ques_obj.question_type,
                    'text': ques_obj.text[user_language], 'isMandatory': ques_obj.isMandatory,
                    'answers': []}
    for answer in ques_obj.answers:
        request_data['answers'].append(answer_json(answer, user_language))
    return request_data


def answer_json(ans_obj, user_language):
    request_data = {'answer_id': ans_obj.answer_id, 'text': ans_obj.text[user_language],
                    'questions': []}
    for sub_question in ans_obj.questions:
        request_data['questions'].append(sub_question_json(sub_question, user_language))
    return request_data


def sub_question_json(sub_ques_obj, user_language):
    request_data = {'question_id': str(sub_ques_obj.question_id), 'question_type': sub_ques_obj.question_type,
                    'text': sub_ques_obj.text[user_language], 'isMandatory': sub_ques_obj.isMandatory,
                    'answers': []}
    for sub_answer in sub_ques_obj.answers:
        request_data['answers'].append(sub_answer_json(sub_answer, user_language))
    return request_data


def sub_answer_json(sub_ans_obj, user_language):
    request_data = {'answer_id': str(sub_ans_obj.answer_id), 'text': sub_ans_obj.text[user_language]}
    return request_data


def questions_dict_func(questions_list):
    questions_dict = {}
    for question in questions_list:
        questions_dict[str(question.id)] = question
    return questions_dict


def questions_list_func(questions_dict, category, user_language):
    request_data = []
    for ques_id in category.questions:
        request_data.append(question_json(questions_dict[ques_id], user_language))
    return request_data
