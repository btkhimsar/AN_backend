from mongoengine import DynamicDocument, fields, EmbeddedDocument


class Answer(EmbeddedDocument):
    ans_id = fields.SequenceField(required=True)
    text = fields.MapField(fields.StringField(max_length=200), required=True)
    questions = fields.ListField(fields.StringField())


class Question(DynamicDocument):
    question_type = fields.StringField(max_length=50, required=True, default="select-one")
    text = fields.MapField(fields.StringField(max_length=100), required=True)
    isMandatory = fields.BooleanField(required=False, default=True)
    answers = fields.EmbeddedDocumentListField(Answer)
