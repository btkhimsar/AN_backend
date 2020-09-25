from mongoengine import Document, fields, EmbeddedDocument


# class SubAnswer(EmbeddedDocument):
#     answer_id = fields.SequenceField()
#     text = fields.MapField(fields.StringField(max_length=200), required=True)
#
#
# class SubQuestion(EmbeddedDocument):
#     question_id = fields.SequenceField()
#     question_type = fields.StringField(max_length=50, required=True, default="select-one")
#     text = fields.MapField(fields.StringField(max_length=200), required=True)
#     isMandatory = fields.BooleanField(required=False, default=True)
#     answers = fields.EmbeddedDocumentListField(SubAnswer)


class Answer(EmbeddedDocument):
    ans_id = fields.SequenceField(required=True)
    text = fields.MapField(fields.StringField(max_length=200), required=True)
    questions = fields.ListField(fields.IntField())
    # questions = fields.EmbeddedDocumentListField(SubQuestion)


class Question(Document):
    _id = fields.IntField(primary_key=True)
    question_type = fields.StringField(max_length=50, required=True, default="select-one")
    text = fields.MapField(fields.StringField(max_length=100), required=True)
    isMandatory = fields.BooleanField(required=False, default=True)
    answers = fields.EmbeddedDocumentListField(Answer)
