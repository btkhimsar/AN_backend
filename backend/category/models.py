from mongoengine import Document, fields, EmbeddedDocument
from Constants.image_urls import HOME_ICON


class Category(Document):
    _id = fields.IntField(primary_key=True)
    name = fields.MapField(fields.StringField(max_length=100), required=True)
    icon_url = fields.URLField(max_length=200, required=True, default=HOME_ICON)
    questions = fields.ListField(fields.StringField(max_length=100))


class SuperCategory(Document):
    _id = fields.IntField(primary_key=True)
    name = fields.MapField(fields.StringField(max_length=100), required=True)
    default_view_count = fields.IntField(min_value=1, max_value=20, required=True, default=5)
    categories = fields.ListField(fields.StringField(max_length=50))


