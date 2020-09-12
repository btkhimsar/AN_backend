from mongoengine import Document, fields, EmbeddedDocument


class SubAnswer(EmbeddedDocument):
    sub_answer_id = fields.IntField()
    text = fields.MapField(fields.StringField(max_length=200), required=True)


class SubQuestion(EmbeddedDocument):
    sub_question_id = fields.IntField()
    sub_question_type = fields.StringField(max_length=50, required=True, default="select-one")
    text = fields.MapField(fields.StringField(max_length=200), required=True)
    isMandatory = fields.BooleanField(required=False, default=True)
    sub_answers = fields.EmbeddedDocumentListField(SubAnswer)


class Answer(EmbeddedDocument):
    answer_id = fields.IntField(required=True)
    text = fields.MapField(fields.StringField(max_length=200), required=True)
    sub_questions = fields.EmbeddedDocumentListField(SubQuestion)


class Question(Document):
    question_type = fields.StringField(max_length=50, required=True, default="select-one")
    text = fields.MapField(fields.StringField(max_length=200), required=True)
    isMandatory = fields.BooleanField(required=False, default=True)
    answers = fields.EmbeddedDocumentListField(Answer)
