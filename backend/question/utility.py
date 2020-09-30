def question_json(ques_obj, language, resp_data, questions_dict):
    request_data = {'question_id': str(ques_obj.id), 'question_type': ques_obj.question_type,
                    'text': ques_obj.text[language], 'isMandatory': ques_obj.isMandatory,
                    'answers': []}
    for answer in ques_obj.answers:
        request_data['answers'].append(answer_json(answer, language, resp_data, questions_dict))
    return request_data


def answer_json(ans_obj, language, resp_data, questions_dict):
    request_data = {'answer_id': ans_obj.ans_id, 'text': ans_obj.text[language],
                    'questions': ans_obj.questions}
    for ques_id in ans_obj.questions:
        resp_data['secondary_questions'][ques_id] = sub_question_json(questions_dict[ques_id], language)
    return request_data


def sub_question_json(sub_ques_obj, language):
    request_data = {'question_id': str(sub_ques_obj.id), 'question_type': sub_ques_obj.question_type,
                    'text': sub_ques_obj.text[language], 'isMandatory': sub_ques_obj.isMandatory,
                    'answers': []}
    for sub_answer in sub_ques_obj.answers:
        request_data['answers'].append(sub_answer_json(sub_answer, language))
    return request_data


def sub_answer_json(sub_ans_obj, language):
    request_data = {'answer_id': sub_ans_obj.ans_id, 'text': sub_ans_obj.text[language]}
    return request_data


def questions_dict_func(questions_list):
    questions_dict = {}
    for question in questions_list:
        questions_dict[str(question.id)] = question
    return questions_dict


def questions_list_func(questions_dict, category, language, resp_data):
    resp_data['primary_questions'] = []
    resp_data['secondary_questions'] = {}
    for ques_id in category.questions:
        resp_data['primary_questions'].append(
            question_json(questions_dict[ques_id], language, resp_data, questions_dict))
