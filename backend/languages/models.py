
from mongoengine import fields, DynamicDocument


class Language(DynamicDocument):
    text = fields.StringField(max_length=200)
    english = fields.StringField(max_length=200)
    hindi = fields.StringField(max_length=200)
