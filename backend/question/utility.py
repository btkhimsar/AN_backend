from .models import Question


def request_json_for_question(question_id, user_language):
    question = Question.objects.get(id=question_id)
    request_data = {}
    request_data['question_id'] = str(question.id)
    request_data['type'] = question.type
    request_data['text'] = question.text[user_language]
    request_data['isMandatory'] = question.isMandatory
    request_data['answers'] = []
    for i in question.answers:
        data = {}
        data['answer_id'] = i.answer_id
        data['text'] = i.text[user_language]
        request_data['answers'].append(data)
    return request_data