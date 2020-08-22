from mongoengine import Document, fields, EmbeddedDocument
from Constants.image_urls import HOME_ICON
from Constants.colors import *

class Category(Document):
    name = fields.MapField(fields.StringField())
    description = fields.MapField(fields.StringField())
    icon_url = fields.URLField(max_length=200, required=True, default=HOME_ICON)
    has_questions = fields.BooleanField(required=True, default=False)
    questions = fields.ListField(fields.StringField(max_length=100))

class SuperCategory(Document):
    name = fields.MapField(fields.StringField(max_length=100, default="", required=True), required=True)
    description = fields.MapField(fields.StringField(max_length=100, default="", required=True), required=True)
    default_view_count = fields.StringField(max_length=20, default="5")
    categories = fields.ListField(fields.StringField(max_length=100))

class SubAnswer(EmbeddedDocument):
    sub_answer_id = fields.IntField()
    text = fields.MapField(fields.StringField(max_length=200, required=True))

class SubQuestion(EmbeddedDocument):
    sub_question_id = fields.IntField()
    type = fields.StringField(max_length=50, required=True, default="select-one")
    text = fields.MapField(fields.StringField(max_length=200, required=True))
    isMandatory = fields.BooleanField(required=False, default=True)
    sub_answers = fields.EmbeddedDocumentListField(SubAnswer)

class Answer(EmbeddedDocument):
    answer_id = fields.IntField(required=True)
    text = fields.MapField(fields.StringField(max_length=200, required=True))
    sub_questions = fields.EmbeddedDocumentListField(SubQuestion)

class Question(Document):
    type = fields.StringField(max_length=50, required=True, default="select-one")
    text = fields.MapField(fields.StringField(max_length=200, required=True))
    isMandatory = fields.BooleanField(required=False, default=True)
    answers = fields.EmbeddedDocumentListField(Answer)

